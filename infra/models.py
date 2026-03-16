from pydantic import BaseModel
from typing import Dict, List, Optional


class ServiceStatus(BaseModel):
    service: str
    status: str  # healthy / degraded / down
    degraded_since: Optional[str] = None
    affected_requests_pct: Optional[int] = None
    affected_users: Optional[int] = None
    affected_departments: Optional[List[str]] = None
    revenue_impact: Optional[str] = None
    notes: Optional[str] = None
    on_call: Optional[str] = None

class Incident(BaseModel):
    incident_id: str
    severity: str  # P1 / P2 / P3
    service: str
    started_at: str
    last_update_at: str
    owner: str
    status: str  # investigating / identified / mitigating
    impact_summary: str
    timeline: List[str]


class AffectedUsersRecord(BaseModel):
    service: str
    affected_users: int


class RevenueImpactRecord(BaseModel):
    service: str
    revenue_impact: str


class CapacityService(BaseModel):
    can_scale: bool


class ClusterCapacity(BaseModel):
    cluster: str
    cpu_util_pct: int
    memory_util_pct: int
    pods_running: int
    services: Optional[Dict[str, CapacityService]] = None
    notes: Optional[str] = None


class Deployment(BaseModel):
    deployment_id: str
    service: str
    version: str
    deployed_at: str
    status: str  # success / failed / rolled_back
    deployed_by: str
    notes: Optional[str] = None


class ScaleResponse(BaseModel):
    scale_request_id: str
    service: str
    action: str
    status: str


class AffectedUsersResponse(BaseModel):
    data: List[AffectedUsersRecord]
    status: str
    timestamp: str


class RevenueImpactResponse(BaseModel):
    data: List[RevenueImpactRecord]
    status: str
    timestamp: str


class CapacityResponse(BaseModel):
    data: List[ClusterCapacity]
    status: str
    timestamp: str
