BASE_INSTRUCTIONS = """
        Understand the USER QUERY using the provided context sections.

        If the query refers to earlier conversation (e.g., "my last query", "previous result"),
        use the CHAT HISTORY section to resolve the reference.

        If answering the query requires data or an action, select the appropriate tool from AVAILABLE TOOLS
        and return a tool call with the correct arguments.
        Prioritize executing the best-fit tool based on your interpretation of the query, and avoid asking
        the user for confirmation unless the request is genuinely ambiguous.

        If the answer can be determined from CHAT HISTORY or reasoning alone, return a normal response.

        Always return a valid JSON object following the schema defined in the system instructions.
    """

TOOL_CALLED_INSTRUCTIONS = """
        A tool was just called and its output has been appended to CHAT HISTORY.

        First, reason over the newest tool output and decide whether it already answers the user query.
        If it does, return a final response and do not call another tool.
        Only call another tool if the current data is insufficient and another tool is strictly necessary.
        Avoid repeating the same tool call with the same arguments unless new information requires it.
        Always return a valid JSON object following the schema in system instructions.
    """

LIMIT_REACHED_INSTRUCTIONS = """
        The LLM call limit has been reached.

        Do not call any tool.
        Acknowledge the limit in plain language.
        Summarize what you attempted and what data you obtained from CHAT HISTORY and tool outputs.
        Return the best possible final answer from the available context only.
        Always return a valid JSON object following the schema in system instructions.
    """
