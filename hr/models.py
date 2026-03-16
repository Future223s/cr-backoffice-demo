from pydantic import BaseModel
from typing import List
from datetime import date

class HeadcountDepartment(BaseModel):
    department: str
    fte: int
    contractors: int

class HeadcountResponse(BaseModel):
    total_fte: int
    total_contractors: int
    departments: List[HeadcountDepartment]


class EmployeeProfile(BaseModel):
    employee_id: str
    name: str
    role: str
    department: str
    manager: str
    tenure_years: float
    employment_type: str  # FTE or Contractor
    email: str
    location: str


class OrgChartNode(BaseModel):
    name: str
    role: str
    reports: List[str]


class OpenPosition(BaseModel):
    role: str
    department: str
    seniority: str
    allocated_budget_usd: int
    hiring_stage: str


class LeaveRequest(BaseModel):
    employee_id: str
    start_date: date
    end_date: date
    reason: str


class LeaveResponse(BaseModel):
    request_id: str
    status: str

class MoveRequest(BaseModel):
    source: str
    destination: str