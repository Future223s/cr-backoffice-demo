from pydantic import BaseModel
from typing import List


class KPI(BaseModel):
    name: str
    value: str
    trend: str  # up / down / flat


class KPIResponse(BaseModel):
    department: str
    kpis: List[KPI]


class Report(BaseModel):
    report_id: str
    title: str
    generated_at: str
    summary: str
    highlights: List[str]


class Anomaly(BaseModel):
    anomaly_id: str
    detected_at: str
    metric: str
    severity: str
    description: str


class QueryRequest(BaseModel):
    query: str