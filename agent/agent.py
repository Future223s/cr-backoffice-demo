from typing import Any, Dict, List
from langgraph.graph import StateGraph, START, END
from google import genai
from pydantic import BaseModel
import httpx
import json
import re
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


class AgentState(BaseModel):
    system_instructions: str
    current_instructions: str
    user_query: str
    chat_history: str = ""
    messages: List[Dict[str, str]] = []
    available_tools: Dict[str, Any] = {}
    working_data: Any = None
    llm_call_count: int = 0
    llm_limit_reached: bool = False
 

class Agent:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model_name: str,
        temperature: float,
        instructions: Dict[str, str],
        tools_prefix: str = "",
        timeout: int = 10,
        llm_call_limit: int = 5,
    ):
        self.base_url = base_url
        self.model_name = model_name
        self.temperature = temperature
        self.instructions = instructions
        self.tools_prefix = tools_prefix.rstrip("/") if tools_prefix else ""
        self.genai_client = genai.Client(api_key=api_key)
        self.async_client = httpx.AsyncClient(timeout=timeout)
        self.graph = self.build_graph()
        self.llm_call_limit = llm_call_limit
        self.last_context = AgentState(
            system_instructions=instructions["system"],
            current_instructions=instructions["base"],
            user_query="",
        )

    def build_graph(self):
        graph = StateGraph(dict)

        graph.add_node("call_llm", self._node_call_llm)
        graph.add_node("execute_tool", self._node_execute_tool)
        graph.add_node("route", self._route_after_llm)
        graph.add_node("return_response", self._node_return_response)

        graph.add_edge(START, "call_llm")
        graph.add_edge("execute_tool", "call_llm")
        graph.add_edge("return_response", END)
        graph.add_conditional_edges(
            "call_llm",
            self._route_after_llm,
            {
                "retry": "call_llm",
                "execute_tool": "execute_tool",
                "return_response": "return_response",
            },
        )

        return graph.compile()

    async def run(self, query: str) -> str:
        context = self.last_context

        context.system_instructions = self.instructions["system"]
        context.current_instructions = self.instructions["base"]
        context.user_query = query
        context.llm_call_count = 0
        context.llm_limit_reached = False

        msg = {"role": "User", "content": query}
        context.messages.append(msg)
        context.chat_history += f"\n{msg['role']}: {msg['content']}"

        if not context.available_tools:
            tools_url = f"{self.base_url}{self.tools_prefix}/tools"
            tools_data: Dict[str, Any] = {}
            try:
                tools_response = await self.async_client.get(tools_url, timeout=10.0)
                tools_response.raise_for_status()
                tools_data = tools_response.json()
                context.available_tools = tools_data.get("data", {})
            except Exception as e:
                logger.debug("FAILED TO FETCH TOOLS: %s", str(e))
                raise Exception(f"Failed to fetch tools: {str(e)}")

        return await self.graph.ainvoke(context)

    async def _node_call_llm(self, context) -> Dict[str, Any]:
        if context.llm_call_count >= self.llm_call_limit + 2:
            context.working_data = self._build_limit_fallback_response(context)
            logger.warning("LLM hard cap reached; returning fallback response.")
            return
        try:
            prompt = self.build_LLM_content(context)
            response = self.genai_client.models.generate_content(model=self.model_name, contents=prompt)

            cleaned_llm_output = re.sub(r"^```(?:json)?|```$", "", response.text.strip(), flags=re.MULTILINE)
            first_brace = cleaned_llm_output.find("{")
            if first_brace != -1:
                cleaned_llm_output = cleaned_llm_output[first_brace:]
            context.working_data = cleaned_llm_output
            context.llm_call_count += 1

            logger.debug("LLM HISTORY: %s", context.chat_history)
            logger.debug("LLM INSTRUCTIONS: %s", context.current_instructions)
            logger.debug("LLM OUTPUT: %s", cleaned_llm_output)
        except Exception as e:
            raise Exception(f"Failed to call LLM: {str(e)}")

    def _route_after_llm(self, context) -> str:
        # Load LLM output as JSON and append required information to history
        try:
            data = json.loads(context.working_data)
            context.working_data = data
        except json.JSONDecodeError as e:
            context.current_instructions = f"The LLM output returned invalid JSON: {e}"
            return "retry"

        msg = {"role": "assistant", "content": data.get("text")}
        context.messages.append(msg)
        context.chat_history += f"\n{msg['role']}: {msg['content']}"

        # Validate required fields
        required_fields = ["return_type", "tool_call", "tool_name", "args", "text", "metadata"]
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            context.current_instructions = f"Retry. Missing required fields: {missing_fields}"
            return "retry"

        if not isinstance(data["text"], str):
            context.current_instructions = "Retry. Text field must be a string"
            return "retry"

        if not isinstance(data["metadata"], dict):
            context.current_instructions = "Retry. Metadata field must be a dict"
            return "retry"

        # No tool call: return response
        if not data["tool_call"]:
            context.messages.append({"role": "assistant", "content": data["text"]})
            return "return_response"

        # Allow exactly one final LLM call with limit instructions to summarize from history.
        if context.llm_call_count >= self.llm_call_limit:
            if not context.llm_limit_reached:
                context.llm_limit_reached = True
                context.current_instructions = self.instructions.get(
                    "limit reached",
                    "LLM call limit reached. Do not call any tools. Summarize what was tried and"
                    " provide the best answer from chat history and tool outputs.",
                )
                logger.warning(
                    "LLM call limit reached (%s); switching to limit-reached instructions.",
                    self.llm_call_limit,
                )
                return "retry"
            context.working_data = json.loads(self._build_limit_fallback_response(context))
            return "return_response"

        # Validate tool exists and arguments are valid
        tool_def = context.available_tools.get(data["tool_name"])
        if not tool_def:
            context.current_instructions = f"No tool was called. tool_name '{data['tool_name']}' not found"
            return "retry"

        if not isinstance(data["args"], dict):
            context.current_instructions = "No tool was called. 'args' field must be a dict"
            return "retry"

        for arg_def in tool_def.get("args", []):
            arg_name = arg_def["name"]
            if arg_def.get("required", True) and arg_name not in data["args"]:
                context.current_instructions = f"Missing arg '{arg_name}'"
                return "retry"

        context.current_instructions = self.instructions["tool called"]
        return "execute_tool"

    async def _node_execute_tool(self, context) -> Dict[str, Any]:
        tool_name = context.working_data.get("tool_name")
        tool_args = context.working_data.get("args", {})
        tool_meta = context.available_tools.get(tool_name)
        tool_method = tool_meta.get("method")

        resolved_url = f"{self.base_url}{tool_meta['path']}"
        payload_args: Dict[str, Any] = {}
        for k, v in tool_args.items():
            placeholder = f"{{{k}}}"
            if placeholder in resolved_url:
                resolved_url = resolved_url.replace(placeholder, str(v))
            else:
                payload_args[k] = v

        try:
            if tool_method == "GET":
                response = await self.async_client.get(resolved_url, params=payload_args, timeout=30.0)
            elif tool_method == "POST":
                response = await self.async_client.post(resolved_url, json=payload_args, timeout=30.0)
            else:
                raise ValueError(f"Unsupported method: {tool_method}")
            response.raise_for_status()
            tool_result = response.json()
        except Exception as e:
            tool_result = {"success": False, "error": str(e)}

        msg = {"role": tool_name, "content": json.dumps(tool_result)}
        context.messages.append(msg)
        context.chat_history += f"\n{msg['role']}: {msg['content']}"

    def _node_return_response(self, context) -> Dict[str, Any]:
        final_response = context.working_data.get("text")
        self.last_context = context
        return final_response

    def build_LLM_content(self, context) -> str:
        sections = [
            ("SYSTEM INSTRUCTIONS", context.system_instructions),
            ("CHAT HISTORY", context.chat_history),
            ("CURRENT USER QUERY:", context.user_query),
            ("CURRENT TASK", context.current_instructions),
            ("AVAILABLE TOOLS", json.dumps(context.available_tools, indent=2)),
        ]
        return "\n\n".join([f"### {title}\n{content}" for title, content in sections])

    def _build_limit_fallback_response(self, context: AgentState) -> str:
        last_tool = self.last_tool_response(context)
        detail = "No tool outputs are available in the current history."
        if last_tool:
            detail = f"Last tool output from {last_tool['role']}: {self.shorten(last_tool['content'])}"
        return json.dumps(
            {
                "return_type": "return_response",
                "tool_call": False,
                "tool_name": None,
                "args": {},
                "text": (
                    "LLM call limit reached. Returning best-effort summary from available history. "
                    + detail
                ),
                "metadata": {"reason": "llm_limit_fallback", "llm_call_limit": self.llm_call_limit},
            }
        )
    
    @staticmethod
    def shorten(text: str, limit: int = 200) -> str:
        if len(text) <= limit:
            return text
        return f"{text[:limit - 3]}..."

    @staticmethod
    def last_tool_response(context: AgentState) -> Dict[str, str] | None:
        for message in reversed(context.messages):
            if message["role"] not in {"User", "assistant"}:
                return message
        return None
