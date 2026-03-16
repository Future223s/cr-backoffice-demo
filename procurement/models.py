from pydantic import BaseModel
from typing import List, Optional


class Vendor(BaseModel):
    vendor_id: str
    name: str
    category: str  # cloud / hardware / professional_services
    risk_tier: str  # low / medium / high
    primary_contact: str
    email: str
    status: str  # approved / under_review


class Contract(BaseModel):
    contract_id: str
    vendor: str
    value_usd: int
    expires_on: str
    days_remaining: int
    owner: str
    renewal_risk: str  # low / medium / high
    notes: Optional[str] = None


class RFQRequest(BaseModel):
    department: str
    category: str
    description: str
    expected_budget_usd: int
    vendor_preference: Optional[str] = None


class RFQResponse(BaseModel):
    rfq_id: str
    status: str