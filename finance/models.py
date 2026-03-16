from pydantic import BaseModel
from typing import List


class BudgetResponse(BaseModel):
    department: str
    fiscal_year: int
    allocated_usd: int
    spent_usd: int
    remaining_usd: int
    burn_rate_pct: int
    fy_months_remaining: int
    risk_level: str


class MonthlySpend(BaseModel):
    month: str
    category: str
    amount_usd: int


class SpendReportResponse(BaseModel):
    fiscal_year: int
    department: str
    monthly_breakdown: List[MonthlySpend]


class Invoice(BaseModel):
    invoice_id: str
    vendor: str
    amount_usd: int
    due_date: str
    status: str


class CostCenter(BaseModel):
    department: str
    budget_code: str


class PurchaseOrderRequest(BaseModel):
    vendor: str
    amount_usd: int
    department: str
    description: str


class PurchaseOrderResponse(BaseModel):
    po_id: str
    status: str