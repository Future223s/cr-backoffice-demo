from shared_resources.prompts import BASE_INSTRUCTIONS, LIMIT_REACHED_INSTRUCTIONS, TOOL_CALLED_INSTRUCTIONS

INSTRUCTIONS = {
    "system": """
        You are an Infrastructure operations agent specialized in service health, incident awareness, capacity tracking, and scaling requests.
        Use the infrastructure endpoints to provide concise status updates or guidance formatted for programmatic workflows.

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

        You have access to infrastructure tools for service health checks, incidents, capacity reports, deployments, and scaling actions.
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
    "get_services_status": {
        "description": "Return service health with optional filters.",
        "method": "GET",
        "path": "/infra/services/status",
        "args": [
            {
                "name": "service",
                "type": "string",
                "required": False,
                "possible_values": [
                    "payments-gateway",
                    "auth-service",
                    "user-service",
                    "orders-service",
                    "ledger-service",
                    "notifications",
                    "reporting-api",
                    "risk-engine",
                    "web-frontend",
                    "admin-portal",
                    "data-pipeline",
                    "audit-service",
                ],
            },
            {
                "name": "status",
                "type": "string",
                "required": False,
                "possible_values": ["healthy", "degraded"],
            },
        ],
    },
    "get_active_incidents": {
        "description": "List active infrastructure incidents.",
        "method": "GET",
        "path": "/infra/incidents/active",
        "args": [],
    },
    "get_capacity": {
        "description": "Return cluster capacity metrics.",
        "method": "GET",
        "path": "/infra/capacity",
        "args": [],
    },
    "get_recent_deployments": {
        "description": "Fetch recent deployments.",
        "method": "GET",
        "path": "/infra/deployments/recent",
        "args": [],
    },
    "scale_service": {
        "description": "Request scaling action for a service.",
        "method": "POST",
        "path": "/infra/scale/{service}",
        "args": [
            {
                "name": "service",
                "type": "string",
                "required": True,
                "possible_values": [
                    "payments-gateway",
                    "auth-service",
                    "user-service",
                    "orders-service",
                    "ledger-service",
                    "notifications",
                    "reporting-api",
                    "risk-engine",
                    "web-frontend",
                    "admin-portal",
                    "data-pipeline",
                    "audit-service",
                ],
            }
        ],
    },
}
