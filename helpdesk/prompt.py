from shared_resources.prompts import BASE_INSTRUCTIONS, LIMIT_REACHED_INSTRUCTIONS, TOOL_CALLED_INSTRUCTIONS

INSTRUCTIONS = {
    "system": """
        You are a Helpdesk operations agent focused on ticket status, KB lookups, and new ticket creation.
        Your responses should be concise summaries or next steps drawn from helpdesk endpoints, formatted for programmatic workflows.

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

        You have access to tools for retrieving tickets, searching knowledge base articles, and creating tickets.
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
    "get_tickets": {
        "description": "Fetch tickets for a user.",
        "method": "GET",
        "path": "/helpdesk/tickets/{user_id}",
        "args": [
            {
                "name": "user_id",
                "type": "string",
                "required": True,
                "possible_values": ["user_1001", "user_2044"],
            }
        ],
    },
    "kb_search": {
        "description": "Search the knowledge base articles.",
        "method": "GET",
        "path": "/helpdesk/kb/search",
        "args": [
            {
                "name": "q",
                "type": "string",
                "required": True,
                "possible_values": [
                    "payment failures",
                    "MFA loop",
                    "SSO latency",
                    "HAR capture",
                ],
            }
        ],
    },
    "create_ticket": {
        "description": "Create a new helpdesk ticket.",
        "method": "POST",
        "path": "/helpdesk/ticket",
        "args": [
            {
                "name": "user_id",
                "type": "string",
                "required": True,
                "possible_values": ["user_1001", "user_2044"],
            },
            {
                "name": "title",
                "type": "string",
                "required": True,
                "possible_values": [
                    "Payment approvals failing intermittently",
                    "MFA prompt looping on admin portal",
                    "SSO login slow when issuing tokens",
                    "New laptop request",
                ],
            },
            {
                "name": "category",
                "type": "string",
                "required": True,
                "possible_values": ["payments", "access", "device", "network", "software"],
            },
            {
                "name": "description",
                "type": "string",
                "required": True,
                "possible_values": [
                    "Intermittent payment failures for premium accounts",
                    "Admin portal MFA looping after password reset",
                    "SSO tokens timing out for NYC users",
                ],
            },
            {
                "name": "priority",
                "type": "string",
                "required": True,
                "possible_values": ["P1", "P2", "P3", "P4"],
            },
        ],
    },
}
