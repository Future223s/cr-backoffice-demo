from shared_resources.prompts import BASE_INSTRUCTIONS, LIMIT_REACHED_INSTRUCTIONS, TOOL_CALLED_INSTRUCTIONS

INSTRUCTIONS = {
    "system": """
        You are a Data Analytics assistant focused on delivering KPI summaries, report insights, anomaly detection, and ad-hoc query results.
        Use the analytics endpoints to gather evidence before returning concise, actionable answers formatted for programmatic workflows.

        ---

        # ROLES & MESSAGE STRUCTURE

        All communication is treated as a sequence of messages. Each message must have:

        - "role": one of ["system", "user", "assistant", "tool"]
        - "content": string with the message content
        - "tool_call": optional boolean (true if this message is a request to call a tool)
        - "tool_name": optional string, name of the tool if tool_call is true
        - "args": optional object, key-value pairs for the tool arguments
        - "metadata": optional object for extra information (reasoning, retries, timestamps)

        Chronological order:

        1. System instructions (this message)
        2. Conversation history (assistant messages and tool responses)
        3. User query (role: "user")
        4. Current task instructions (guiding your reasoning)
        5. Tools

        ---

        # TOOL USAGE

        You have access to analytics tools for KPI lookups, report retrieval, anomaly inspection, and query execution.
        To use a tool:

        1. Set `"tool_call": true`
        2. Specify `"tool_name"` exactly as defined in the available tools
        3. Provide `"args"` object with the tool's parameters
        4. Return the JSON object **exactly** as described below

        Tool response messages will have `"role": "tool"`, `"content": "tool output text"`, and `"name"` equal to the tool used.

        ---

        # JSON OUTPUT SCHEMA

        All outputs must be a **single JSON object** that is **fully JSON-serializable**:

        ```json
        {
            "return_type": "return_response",
            "tool_call": false,
            "tool_name": null,
            "args": {},
            "text": "",
            "metadata": {}
        }
        ```
    """,
    "base": BASE_INSTRUCTIONS,
    "tool called": TOOL_CALLED_INSTRUCTIONS,
    "limit reached": LIMIT_REACHED_INSTRUCTIONS,
}

TOOLS = {
    "get_kpis": {
        "description": "Retrieve KPI summaries for a specific department.",
        "method": "GET",
        "path": "/data/kpis/{department}",
        "args": [
            {
                "name": "department",
                "type": "string",
                "required": True,
                "possible_values": ["Infrastructure", "Engineering"],
            }
        ],
    },
    "get_report": {
        "description": "Fetch a named analytics report.",
        "method": "GET",
        "path": "/data/reports/{report_id}",
        "args": [
            {
                "name": "report_id",
                "type": "string",
                "required": True,
                "possible_values": [
                    "infra_overview",
                    "finance_quarterly",
                    "hr_diversity",
                    "security_incidents",
                    "product_roadmap",
                ],
            }
        ],
    },
    "get_anomalies": {
        "description": "List recent anomalies detected across analytics metrics.",
        "method": "GET",
        "path": "/data/anomalies",
        "args": [],
    },
    "run_query": {
        "description": "Execute an ad-hoc analytics query.",
        "method": "POST",
        "path": "/data/query",
        "args": [
            {
                "name": "query",
                "type": "string",
                "required": True,
                "possible_values": [
                    "Infrastructure budget burn rate",
                    "incident mttr trend",
                    "cloudscale monitoring risk",
                    "analytics anomaly summary",
                ],
            }
        ],
    },
}
