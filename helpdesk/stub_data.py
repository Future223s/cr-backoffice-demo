TICKETS_BY_USER = {
    "user_1001": [
        {
            "ticket_id": "tkt_2025_4012",
            "user_id": "user_1001",
            "title": "Payment approvals failing intermittently",
            "status": "in_progress",
            "priority": "P2",
            "created_at": "2025-02-25T14:35:00Z",
            "last_updated_at": "2025-02-25T15:02:00Z",
            "category": "payments",
            "assigned_to": "Helpdesk - Tier 2",
            "notes": "Correlates with payments-gateway degraded status; asked user to retry after mitigation window.",
        },
        {
            "ticket_id": "tkt_2025_3988",
            "user_id": "user_1001",
            "title": "MFA prompt looping on admin portal",
            "status": "waiting_on_user",
            "priority": "P3",
            "created_at": "2025-02-24T09:18:00Z",
            "last_updated_at": "2025-02-25T10:05:00Z",
            "category": "access",
            "assigned_to": "Helpdesk - Tier 1",
            "notes": "Likely token refresh issue; requested browser HAR + device details.",
        },
    ],
    "user_2044": [
        {
            "ticket_id": "tkt_2025_4025",
            "user_id": "user_2044",
            "title": "SSO login slow when issuing tokens",
            "status": "open",
            "priority": "P3",
            "created_at": "2025-02-25T11:04:00Z",
            "last_updated_at": "2025-02-25T11:04:00Z",
            "category": "access",
            "assigned_to": "Helpdesk - Tier 1",
            "notes": "Possible auth-service latency issue; monitoring incident inc_p2_017.",
        }
    ],
}

KB_ARTICLES = [
    {
        "article_id": "kb_102",
        "title": "Troubleshooting intermittent payment failures",
        "tags": ["payments", "gateway", "5xx", "timeouts"],
        "last_updated_at": "2025-02-25T12:20:00Z",
        "summary": "Steps to identify whether payment failures are user-side, merchant-side, or linked to payments-gateway incidents.",
    },
    {
        "article_id": "kb_088",
        "title": "Admin Portal MFA loop: cache & token reset steps",
        "tags": ["admin-portal", "mfa", "auth", "cookies"],
        "last_updated_at": "2025-02-20T08:10:00Z",
        "summary": "Guidance for resolving repeated MFA prompts, including clearing session cookies and resetting tokens.",
    },
    {
        "article_id": "kb_074",
        "title": "SSO latency checklist (Auth-Service)",
        "tags": ["sso", "auth-service", "latency", "p95"],
        "last_updated_at": "2025-02-25T10:30:00Z",
        "summary": "How to verify SSO latency symptoms, gather diagnostics, and correlate with incident timelines.",
    },
    {
        "article_id": "kb_061",
        "title": "How to capture a HAR file for troubleshooting",
        "tags": ["har", "browser", "troubleshooting"],
        "last_updated_at": "2025-01-12T09:00:00Z",
        "summary": "Instructions for capturing HAR logs in Chrome/Edge to help diagnose portal issues.",
    },
]