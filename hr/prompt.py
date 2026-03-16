from shared_resources.prompts import BASE_INSTRUCTIONS, LIMIT_REACHED_INSTRUCTIONS, TOOL_CALLED_INSTRUCTIONS

INSTRUCTIONS = {
    "system": """
        You are an HR assistant agent specialized in providing accurate, concise, and actionable summaries
        of employee information, headcount, organizational charts, open positions, and leave requests. 
        Your goal is to assist the user by querying HR-related endpoints and returning structured outputs 
        suitable for programmatic workflows.

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

        You have access to certain tools to retrieve HR data (like headcount, employee details, org charts, 
        open positions, or leave requests). To use a tool:

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
            "return_type": "return_response",    // always "return_response" when returning a final answer
            "tool_call": false,                  // true if agent wants to call a tool
            "tool_name": null,                   // tool name if tool_call is true
            "args": {},                          // key-value arguments for the tool
            "text": "",                          // human-readable message or summary
            "metadata": {}                        // optional info: reasoning steps, retries, timestamps, confidence
        }
        ```
    """,
    "base": BASE_INSTRUCTIONS,
    "tool called": TOOL_CALLED_INSTRUCTIONS,
    "limit reached": LIMIT_REACHED_INSTRUCTIONS,
}



TOOLS = {
    "list_files": {
        "description": "List all files available in the workspace.",
        "method": "GET",
        "path": "/hr/files",
        "args": []
    },
    "move_file": {
        "description": "Move a file from one location to the accepted folder within the workspace.",
        "method": "POST",
        "path": "/hr/files/accept",
        "args": [
            {"name": "source", "type": "string", "required": True,
            "description": "Source file path"},
        ]
    },
    "delete_file": {
        "description": "Read the contents of a file from the workspace.",
        "method": "GET",
        "path": "/hr/files/delete",
        "args": [
            {"name": "path", "type": "string", "required": True,
            "description": "Relative path to the file in the workspace"}
        ]
    },
    "get_headcount": {
        "description": "Get total headcount with optional filters.",
        "method": "GET",
        "path": "/hr/headcount",
        "args": [
            {"name": "departments", "type": "list[str]", "required": False,
             "possible_values": ["Infrastructure", "Engineering", "Finance", "Data", "HR", "Support"]},
            {"name": "employment_type", "type": "string", "required": False,
             "possible_values": ["FTE", "Contractor"]},
        ],
    },

    "get_employee": {
        "description": "Retrieve employee details by employee ID.",
        "method": "GET",
        "path": "/hr/employees/{employee_id}",
        "args": [
            {"name": "employee_id", "type": "string", "required": True,
             "possible_values": ["emp_001", "emp_002", "emp_003", "emp_004", "emp_005", "emp_006", "emp_007"]},
        ],
    },

    "get_org_chart": {
        "description": "Return the organizational chart for a department.",
        "method": "GET",
        "path": "/hr/org-chart/{department}",
        "args": [
            {"name": "department", "type": "string", "required": True,
             "possible_values": ["Infrastructure", "Engineering", "Finance", "Data", "HR", "Support"]},
        ],
    },

    "get_open_positions": {
        "description": "List open positions with optional filters.",
        "method": "GET",
        "path": "/hr/open-positions",
        "args": [
            {"name": "role", "type": "string", "required": False,
             "possible_values": [
                 "Senior Infrastructure Engineer", "Junior SRE", "Junior Data Analyst",
                 "Senior Product Manager", "DevOps Engineer", "Data Scientist",
                 "Financial Analyst", "HR Business Partner", "Security Engineer",
                 "QA Automation Engineer", "Business Intelligence Analyst", "Cloud Solutions Architect"
             ]},
            {"name": "department", "type": "string", "required": False,
             "possible_values": ["Infrastructure", "Engineering", "Finance", "Data", "HR"]},
            {"name": "seniority", "type": "string", "required": False,
             "possible_values": ["Junior", "Mid", "Senior"]},
            {"name": "hiring_stage", "type": "string", "required": False,
             "possible_values": [
                 "Screening", "Phone Screen", "Technical Assessment", "Technical Interview",
                 "Panel Interview", "Final Interview", "Initial Review", "Offer Pending",
                 "Offer Extended", "Background Check"
             ]},
            {"name": "min_budget", "type": "integer", "required": False,
             "possible_values": [80000, 85000, 90000, 95000, 110000, 120000, 130000, 135000, 160000, 175000, 180000]},
            {"name": "max_budget", "type": "integer", "required": False,
             "possible_values": [80000, 85000, 90000, 95000, 110000, 120000, 130000, 135000, 160000, 175000, 180000]},
        ],
    },

    "request_leave": {
        "description": "Submit a leave request for an employee.",
        "method": "POST",
        "path": "/hr/leave/request",
        "args": [
            {"name": "employee_id", "type": "string", "required": True,
             "possible_values": ["emp_001", "emp_002", "emp_003", "emp_004", "emp_005", "emp_006", "emp_007"]},
            {"name": "start_date", "type": "string", "required": True,
             "possible_values": ["2025-03-03", "2025-03-10", "2025-03-15", "2025-03-20", "2025-03-25", "2025-03-28", "2025-04-01", "2025-04-10"]},
            {"name": "end_date", "type": "string", "required": True,
             "possible_values": ["2025-03-07", "2025-03-14", "2025-03-16", "2025-03-22", "2025-03-26", "2025-03-28", "2025-04-05", "2025-04-18"]},
            {"name": "reason", "type": "string", "required": False,
             "possible_values": ["Medical leave", "Annual vacation", "Personal day", "Family emergency", "Maternity leave", "Doctor appointment", "Bereavement leave"]},
        ],
    },
}
