from datetime import datetime

# ----------------------------
# KPIs
# ----------------------------

KPIS = {
    "Infrastructure": {
        "department": "Infrastructure",
        "kpis": [
            {"name": "Deployment Frequency", "value": "+12% QoQ", "trend": "up"},
            {"name": "Mean Time To Recovery (MTTR)", "value": "-8%", "trend": "down"},
            {"name": "Incident Rate", "value": "+23%", "trend": "up"},
            {"name": "Cloud Cost Growth", "value": "+14%", "trend": "up"},
            {"name": "System Availability", "value": "99.82%", "trend": "flat"},
        ],
    },
    "Engineering": {
        "department": "Engineering",
        "kpis": [
            {"name": "Feature Delivery Velocity", "value": "+9%", "trend": "up"},
            {"name": "Bug Resolution Time", "value": "-6%", "trend": "down"},
            {"name": "Code Coverage", "value": "84%", "trend": "up"},
            {"name": "Tech Debt Ratio", "value": "18%", "trend": "flat"},
            {"name": "Release Rollbacks", "value": "2 this quarter", "trend": "down"},
        ],
    },
}

# ----------------------------
# Reports
# ----------------------------

REPORTS = {
    "infra_overview": {
        "report_id": "infra_overview",
        "title": "Infrastructure Operational Overview",
        "generated_at": "2025-02-25T09:30:00Z",
        "summary": "Infrastructure is under moderate operational strain with elevated incident rate and rising cloud spend.",
        "highlights": [
            "Incident rate increased by 23% compared to last quarter.",
            "MTTR improved by 8%, mitigating downtime impact.",
            "Cloud hosting costs increased month-over-month.",
            "API error spike detected at 02:00 UTC."
        ],
    },
    "finance_quarterly": {
        "report_id": "finance_quarterly",
        "title": "Q4 2024 Financial Performance Report",
        "generated_at": "2025-01-15T14:00:00Z",
        "summary": "Strong quarterly performance with 18% revenue growth, though operating expenses increased by 12%.",
        "highlights": [
            "Revenue exceeded targets by 5% with $2.8M in quarterly earnings.",
            "Customer acquisition cost increased by 8% due to market competition.",
            "Gross margins improved to 68% through vendor negotiation.",
            "Cash runway extended to 24 months with recent funding round."
        ],
    },
    "hr_diversity": {
        "report_id": "hr_diversity",
        "title": "Workforce Diversity & Inclusion Report",
        "generated_at": "2025-02-01T10:00:00Z",
        "summary": "Diversity metrics show improvement in representation but retention gaps persist in underrepresented groups.",
        "highlights": [
            "Women in leadership roles increased to 42% (target: 45%).",
            "Underrepresented minorities comprise 28% of workforce (target: 35%).",
            "Employee satisfaction scores improved by 6% across all demographics.",
            "Voluntary turnover rate decreased by 3% but remains higher for junior roles."
        ],
    },
    "security_incidents": {
        "report_id": "security_incidents",
        "title": "Security Incident Response Report",
        "generated_at": "2025-02-20T16:30:00Z",
        "summary": "Two security incidents handled successfully with no data breach. Response times within SLA.",
        "highlights": [
            "Phishing attempt blocked with zero successful compromises.",
            "DDoS attack mitigated within 12 minutes of detection.",
            "Security training completion rate reached 94%.",
            "Zero critical vulnerabilities found in recent penetration testing."
        ],
    },
    "product_roadmap": {
        "report_id": "product_roadmap",
        "title": "Q1 2025 Product Roadmap Progress",
        "generated_at": "2025-02-28T11:00:00Z",
        "summary": "Product roadmap is 78% complete with two major features delayed due to technical dependencies.",
        "highlights": [
            "Mobile app redesign completed and deployed to 100% of users.",
            "API rate limiting feature delivered ahead of schedule.",
            "Real-time analytics dashboard delayed by 2 weeks due to data pipeline issues.",
            "Customer feedback integration showing 15% improvement in feature adoption."
        ],
    }
}

# ----------------------------
# Anomalies
# ----------------------------

ANOMALIES = [
    {
        "anomaly_id": "an_2025_204",
        "detected_at": "2025-02-25T02:00:00Z",
        "metric": "API Error Rate",
        "severity": "high",
        "description": "Unusual spike in 5xx responses reaching 12% of traffic for 18 minutes.",
    },
    {
        "anomaly_id": "an_2025_205",
        "detected_at": "2025-02-24T14:30:00Z",
        "metric": "Database Connection Pool",
        "severity": "medium",
        "description": "Connection pool utilization exceeded 95% for 45 minutes, causing request queuing.",
    },
    {
        "anomaly_id": "an_2025_206",
        "detected_at": "2025-02-23T09:15:00Z",
        "metric": "User Login Attempts",
        "severity": "low",
        "description": "Unusual pattern of failed login attempts from single IP address (potential brute force).",
    },
    {
        "anomaly_id": "an_2025_207",
        "detected_at": "2025-02-22T16:45:00Z",
        "metric": "Payment Processing Latency",
        "severity": "high",
        "description": "Payment processing time increased by 300% for 22 minutes, affecting checkout flow.",
    },
    {
        "anomaly_id": "an_2025_208",
        "detected_at": "2025-02-21T11:20:00Z",
        "metric": "Cache Hit Rate",
        "severity": "medium",
        "description": "Cache hit rate dropped below 60% for 38 minutes, increasing database load.",
    },
    {
        "anomaly_id": "an_2025_209",
        "detected_at": "2025-02-20T08:10:00Z",
        "metric": "File Upload Size",
        "severity": "low",
        "description": "Average file upload size increased by 45% compared to 7-day baseline.",
    },
    {
        "anomaly_id": "an_2025_210",
        "detected_at": "2025-02-19T13:55:00Z",
        "metric": "Email Delivery Rate",
        "severity": "medium",
        "description": "Email delivery rate dropped to 89% for 2 hours, potential SMTP provider issues.",
    }
]