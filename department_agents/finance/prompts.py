from shared_resources.prompts import BASE_INSTRUCTIONS, LIMIT_REACHED_INSTRUCTIONS, TOOL_CALLED_INSTRUCTIONS

INSTRUCTIONS = {
    "system": """
        You are a Finance operations assistant focused on budgets, spend reports, invoices, and purchase orders.
        Surface concise, numbers-backed answers by querying finance endpoints and return outputs structured for programmatic workflows.

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

        You have access to finance tools for budgets, spend reports, pending invoices, cost centers, and purchase orders.
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
    "get_budget": {
        "description": "Retrieve the fiscal budget for a department and year.",
        "method": "GET",
        "path": "/finance/budget/{department}/{fy}",
        "args": [
            {
                "name": "department",
                "type": "string",
                "required": True,
                "possible_values": ["Infrastructure", "Engineering"],
            },
            {
                "name": "fy",
                "type": "integer",
                "required": True,
                "possible_values": [2025],
            },
        ],
    },
    "get_spend_report": {
        "description": "Fetch the latest spend report for a department.",
        "method": "GET",
        "path": "/finance/spend-report",
        "args": [
            {
                "name": "department",
                "type": "string",
                "required": True,
                "possible_values": ["Infrastructure", "Engineering"],
            }
        ],
    },
    "get_pending_invoices": {
        "description": "List all pending invoices.",
        "method": "GET",
        "path": "/finance/invoices/pending",
        "args": [],
    },
    "get_cost_centers": {
        "description": "Return cost center mappings.",
        "method": "GET",
        "path": "/finance/cost-centers",
        "args": [],
    },
    "raise_purchase_order": {
        "description": "Create a purchase order request.",
        "method": "POST",
        "path": "/finance/purchase-order",
        "args": [
            {
                "name": "vendor",
                "type": "string",
                "required": True,
                "possible_values": [
                    "CloudScale Solutions",
                    "SecureNet Systems",
                    "DataForge Analytics",
                    "IronRack Hardware",
                ],
            },
            {
                "name": "amount_usd",
                "type": "integer",
                "required": True,
                "possible_values": [45000, 82000, 150000],
            },
            {
                "name": "department",
                "type": "string",
                "required": True,
                "possible_values": ["Infrastructure", "Engineering", "Finance", "Data"],
            },
            {
                "name": "description",
                "type": "string",
                "required": True,
                "possible_values": [
                    "Purchase new monitoring license",
                    "Hardware refresh for ledger cluster",
                    "Professional services engagement for compliance",
                ],
            },
        ],
    },
}
