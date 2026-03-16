from datetime import date

# ----------------------------
# Headcount
# ----------------------------

HEADCOUNT = {
    "total_fte": 128,
    "total_contractors": 18,
    "departments": [
        {"department": "Infrastructure", "fte": 42, "contractors": 8},
        {"department": "Engineering", "fte": 38, "contractors": 5},
        {"department": "Finance", "fte": 15, "contractors": 1},
        {"department": "Data", "fte": 18, "contractors": 2},
        {"department": "HR", "fte": 8, "contractors": 1},
        {"department": "Support", "fte": 7, "contractors": 1},
    ],
}

# ----------------------------
# Employees (20 seeded)
# ----------------------------

EMPLOYEES = {
    "emp_001": {
        "employee_id": "emp_001",
        "name": "Ayesha Khan",
        "role": "VP Infrastructure",
        "department": "Infrastructure",
        "manager": "CTO",
        "tenure_years": 4.2,
        "employment_type": "FTE",
        "email": "ayesha.khan@company.com",
        "location": "Karachi",
    },
    "emp_002": {
        "employee_id": "emp_002",
        "name": "Bilal Ahmed",
        "role": "Senior SRE",
        "department": "Infrastructure",
        "manager": "Ayesha Khan",
        "tenure_years": 3.1,
        "employment_type": "FTE",
        "email": "bilal.ahmed@company.com",
        "location": "Lahore",
    },
    "emp_003": {
        "employee_id": "emp_003",
        "name": "Priya Nair",
        "role": "Site Reliability Engineer",
        "department": "Infrastructure",
        "manager": "Bilal Ahmed",
        "tenure_years": 2.4,
        "employment_type": "FTE",
        "email": "priya.nair@company.com",
        "location": "Bangalore",
    },
    "emp_004": {
        "employee_id": "emp_004",
        "name": "Omar Siddiqui",
        "role": "Cloud Architect (Contractor)",
        "department": "Infrastructure",
        "manager": "Ayesha Khan",
        "tenure_years": 1.2,
        "employment_type": "Contractor",
        "email": "omar.siddiqui@company.com",
        "location": "Dubai",
    },
    # Add more across departments
    "emp_005": {
        "employee_id": "emp_005",
        "name": "Sara Williams",
        "role": "Head of Data",
        "department": "Data",
        "manager": "CPO",
        "tenure_years": 3.8,
        "employment_type": "FTE",
        "email": "sara.williams@company.com",
        "location": "London",
    },
    "emp_006": {
        "employee_id": "emp_006",
        "name": "Hassan Raza",
        "role": "Data Engineer",
        "department": "Data",
        "manager": "Sara Williams",
        "tenure_years": 1.6,
        "employment_type": "FTE",
        "email": "hassan.raza@company.com",
        "location": "Islamabad",
    },
    "emp_007": {
        "employee_id": "emp_007",
        "name": "Emily Chen",
        "role": "Product Manager",
        "department": "Engineering",
        "manager": "CPO",
        "tenure_years": 2.9,
        "employment_type": "FTE",
        "email": "emily.chen@company.com",
        "location": "Singapore",
    },
}

# ----------------------------
# Open Positions
# ----------------------------

OPEN_POSITIONS = [
    {
        "role": "Senior Infrastructure Engineer",
        "department": "Infrastructure",
        "seniority": "Senior",
        "allocated_budget_usd": 180000,
        "hiring_stage": "Final Interview",
    },
    {
        "role": "Junior SRE",
        "department": "Infrastructure",
        "seniority": "Junior",
        "allocated_budget_usd": 95000,
        "hiring_stage": "Screening",
    },
    {
        "role": "Junior Data Analyst",
        "department": "Data",
        "seniority": "Junior",
        "allocated_budget_usd": 85000,
        "hiring_stage": "Offer Pending",
    },
    {
        "role": "Senior Product Manager",
        "department": "Engineering",
        "seniority": "Senior",
        "allocated_budget_usd": 160000,
        "hiring_stage": "Technical Interview",
    },
    {
        "role": "DevOps Engineer",
        "department": "Infrastructure",
        "seniority": "Mid",
        "allocated_budget_usd": 120000,
        "hiring_stage": "Phone Screen",
    },
    {
        "role": "Data Scientist",
        "department": "Data",
        "seniority": "Mid",
        "allocated_budget_usd": 130000,
        "hiring_stage": "Offer Extended",
    },
    {
        "role": "Financial Analyst",
        "department": "Finance",
        "seniority": "Mid",
        "allocated_budget_usd": 90000,
        "hiring_stage": "Background Check",
    },
    {
        "role": "HR Business Partner",
        "department": "HR",
        "seniority": "Senior",
        "allocated_budget_usd": 110000,
        "hiring_stage": "Initial Review",
    },
    {
        "role": "Security Engineer",
        "department": "Infrastructure",
        "seniority": "Mid",
        "allocated_budget_usd": 135000,
        "hiring_stage": "Final Interview",
    },
    {
        "role": "QA Automation Engineer",
        "department": "Engineering",
        "seniority": "Junior",
        "allocated_budget_usd": 80000,
        "hiring_stage": "Technical Assessment",
    },
    {
        "role": "Business Intelligence Analyst",
        "department": "Data",
        "seniority": "Mid",
        "allocated_budget_usd": 95000,
        "hiring_stage": "Panel Interview",
    },
    {
        "role": "Cloud Solutions Architect",
        "department": "Infrastructure",
        "seniority": "Senior",
        "allocated_budget_usd": 175000,
        "hiring_stage": "Offer Pending",
    }
]

# ----------------------------
# Leave Tracking
# ----------------------------

PENDING_LEAVE = {
    "emp_003": {
        "start_date": date(2025, 3, 3),
        "end_date": date(2025, 3, 7),
        "reason": "Medical leave",
        "status": "pending",
    },
    "emp_007": {
        "start_date": date(2025, 3, 10),
        "end_date": date(2025, 3, 14),
        "reason": "Annual vacation",
        "status": "approved",
    },
    "emp_012": {
        "start_date": date(2025, 3, 15),
        "end_date": date(2025, 3, 16),
        "reason": "Personal day",
        "status": "pending",
    },
    "emp_005": {
        "start_date": date(2025, 3, 20),
        "end_date": date(2025, 3, 22),
        "reason": "Family emergency",
        "status": "approved",
    },
    "emp_009": {
        "start_date": date(2025, 4, 1),
        "end_date": date(2025, 4, 5),
        "reason": "Maternity leave",
        "status": "approved",
    },
    "emp_015": {
        "start_date": date(2025, 3, 25),
        "end_date": date(2025, 3, 26),
        "reason": "Doctor appointment",
        "status": "pending",
    },
    "emp_002": {
        "start_date": date(2025, 4, 10),
        "end_date": date(2025, 4, 18),
        "reason": "Annual vacation",
        "status": "pending",
    },
    "emp_011": {
        "start_date": date(2025, 3, 28),
        "end_date": date(2025, 3, 28),
        "reason": "Bereavement leave",
        "status": "approved",
    }
}