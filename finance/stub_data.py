from datetime import datetime

# ----------------------------
# Budgets
# ----------------------------

BUDGETS = {
    ("Infrastructure", 2025): {
        "department": "Infrastructure",
        "fiscal_year": 2025,
        "allocated_usd": 4200000,
        "spent_usd": 3100000,
        "remaining_usd": 1100000,
        "burn_rate_pct": 74,
        "fy_months_remaining": 3,
        "risk_level": "elevated",
    },
    ("Engineering", 2025): {
        "department": "Engineering",
        "fiscal_year": 2025,
        "allocated_usd": 6800000,
        "spent_usd": 3940000,
        "remaining_usd": 2860000,
        "burn_rate_pct": 58,
        "fy_months_remaining": 3,
        "risk_level": "stable",
    },
}

# ----------------------------
# Spend Report
# ----------------------------

SPEND_REPORTS = {
    "Infrastructure": {
        "fiscal_year": 2025,
        "department": "Infrastructure",
        "monthly_breakdown": [
            {"month": "Jan", "category": "Cloud Hosting", "amount_usd": 410000},
            {"month": "Feb", "category": "Cloud Hosting", "amount_usd": 435000},
            {"month": "Mar", "category": "Cloud Hosting", "amount_usd": 470000},
            {"month": "Mar", "category": "Security Tooling", "amount_usd": 120000},
        ],
    }
}

# ----------------------------
# Pending Invoices
# ----------------------------

PENDING_INVOICES = [
    {
        "invoice_id": "inv_2025_8821",
        "vendor": "CloudScale Solutions",
        "amount_usd": 84000,
        "due_date": "2025-03-15",
        "status": "awaiting_approval",
    },
    {
        "invoice_id": "inv_2025_8822",
        "vendor": "SecureNet Systems",
        "amount_usd": 27000,
        "due_date": "2025-03-05",
        "status": "processing",
    },
]

# ----------------------------
# Cost Centers
# ----------------------------

COST_CENTERS = [
    {"department": "Infrastructure", "budget_code": "CC-INF-042"},
    {"department": "Engineering", "budget_code": "CC-ENG-021"},
    {"department": "Finance", "budget_code": "CC-FIN-009"},
    {"department": "Data", "budget_code": "CC-DAT-015"},
]