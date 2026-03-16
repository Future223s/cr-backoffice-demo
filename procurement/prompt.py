from shared_resources.prompts import BASE_INSTRUCTIONS, LIMIT_REACHED_INSTRUCTIONS, TOOL_CALLED_INSTRUCTIONS

INSTRUCTIONS = {
    "system": """
        You are a Procurement intelligence agent specializing in vendor relationships, contract renewals, and RFQ tracking.
        Your goal is to surface concise summaries, risk insights, and supported next steps by hitting procurement endpoints
        and returning structured outputs suitable for programmatic workflows.

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

        You have access to tools that return vendor data, expiring contracts, and RFQ confirmations.
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
    "get_vendors": {
        "description": "List vendors with optional filters.",
        "method": "GET",
        "path": "/procurement/vendors",
        "args": [
            {
                "name": "name",
                "type": "string",
                "required": False,
                "possible_values": [
                    "CloudScale Solutions",
                    "SecureNet Systems",
                    "DataForge Analytics",
                    "IronRack Hardware",
                    "NetPulse Monitoring",
                    "Vertex CDN",
                    "QuantumOps Consulting",
                    "ShieldKey IAM",
                ],
            },
            {
                "name": "category",
                "type": "string",
                "required": False,
                "possible_values": ["cloud", "hardware", "professional_services"],
            },
            {
                "name": "risk_tier",
                "type": "string",
                "required": False,
                "possible_values": ["low", "medium", "high"],
            },
            {
                "name": "status",
                "type": "string",
                "required": False,
                "possible_values": ["approved", "under_review"],
            },
        ],
    },
    "get_expiring_contracts": {
        "description": "Return expiring contracts within the next quarter.",
        "method": "GET",
        "path": "/procurement/contracts/expiring",
        "args": [],
    },
    "submit_rfq": {
        "description": "Submit an RFQ to kick off procurement coordination.",
        "method": "POST",
        "path": "/procurement/rfq",
        "args": [
            {
                "name": "department",
                "type": "string",
                "required": True,
                "possible_values": ["Infrastructure", "Engineering", "Finance", "Data", "HR"],
            },
            {
                "name": "category",
                "type": "string",
                "required": True,
                "possible_values": ["cloud", "hardware", "professional_services"],
            },
            {
                "name": "description",
                "type": "string",
                "required": True,
                "possible_values": [
                    "Scale monitoring capacity for payments-gateway",
                    "Purchase GPU compute nodes",
                    "Onboard new professional services vendor for audits",
                    "Renew hardware refresh for backend stack",
                ],
            },
            {
                "name": "expected_budget_usd",
                "type": "integer",
                "required": True,
                "possible_values": [50000, 80000, 120000, 220000],
            },
            {
                "name": "vendor_preference",
                "type": "string",
                "required": False,
                "possible_values": [
                    "CloudScale Solutions",
                    "SecureNet Systems",
                    "DataForge Analytics",
                    "IronRack Hardware",
                    "NetPulse Monitoring",
                    "Vertex CDN",
                    "QuantumOps Consulting",
                    "ShieldKey IAM",
                ],
            },
        ],
    },
}
