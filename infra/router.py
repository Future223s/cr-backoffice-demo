from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import JSONResponse
import os
import traceback
from datetime import datetime
from typing import Optional

from limiter import limiter

from .stub_data import (
    SERVICES_STATUS,
    ACTIVE_INCIDENTS,
    CAPACITY,
    RECENT_DEPLOYMENTS,
)

from .prompt import INSTRUCTIONS, TOOLS
from .models import AffectedUsersResponse, RevenueImpactResponse, CapacityResponse
from deps import success
from agent.agent import Agent

router = APIRouter()

agent = Agent(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=f"http://127.0.0.1:{os.getenv('PORT', '8000')}",
    model_name=os.getenv("GEMINI_MODEL_DEV", "gemini-2.5-flash-lite"),
    temperature=os.getenv("TEMPERATURE_DEV", 0.2),
    instructions=INSTRUCTIONS,
    tools_prefix="/infra",
)


@router.get("/agent")
@limiter.limit("5/minute")
async def run_agent(query: str, request: Request):
    try:
        result = await agent.run(query=query)
        return success(data={"result": result, "query": query})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc(),
            },
        )


@router.get("/tools")
@limiter.limit("60/minute")
async def list_tools(request: Request):
    return success(TOOLS)


def envelope(data):
    return {
        "data": data,
        "status": "success",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

@router.get("/services/status")
@limiter.limit("60/minute")
def get_services_status(
    request: Request,
    service: Optional[str] = Query(None, description="Filter by service name (case-insensitive)"),
    status: Optional[str] = Query(None, description="Filter by health status (case-insensitive)")
):
    # Start with all services
    filtered_services = SERVICES_STATUS.copy()
    
    # Apply filters step by step using raw parameters
    if service:
        filtered_services = [
            svc for svc in filtered_services 
            if service.lower() in svc["service"].lower()
        ]
    
    if status:
        filtered_services = [
            svc for svc in filtered_services 
            if svc["status"].lower() == status.lower()
        ]
    
    return envelope(filtered_services)


@router.get("/incidents/active")
@limiter.limit("40/minute")
def get_active_incidents(request: Request):
    return envelope(ACTIVE_INCIDENTS)


@router.get("/incidents/affected_users", response_model=AffectedUsersResponse)
@limiter.limit("40/minute")
def get_active_affected_users(request: Request) -> AffectedUsersResponse:
    data = [
        {"service": svc["service"], "affected_users": svc.get("affected_users", 0)}
        for svc in SERVICES_STATUS
    ]
    return envelope(data)


@router.get("/incidents/revenue_impact", response_model=RevenueImpactResponse)
@limiter.limit("40/minute")
def get_active_affected_revenue(request: Request) -> RevenueImpactResponse:
    data = [
        {"service": svc["service"], "revenue_impact": svc.get("revenue_impact", "$0/hour")}
        for svc in SERVICES_STATUS
    ]
    return envelope(data)


@router.get("/capacity", response_model=CapacityResponse)
@limiter.limit("30/minute")
def get_capacity(request: Request) -> CapacityResponse:
    return envelope(CAPACITY)


@router.get("/deployments/recent")
@limiter.limit("30/minute")
def get_recent_deployments(request: Request):
    return envelope(RECENT_DEPLOYMENTS)


@router.post("/scale/{service}")
@limiter.limit("15/minute")
def scale_service(service: str, request: Request):
    known_services = {s["service"] for s in SERVICES_STATUS}
    if service not in known_services:
        raise HTTPException(status_code=404, detail="Service not found")

    return envelope(
        {
            "scale_request_id": "scale_2025_031",
            "service": service,
            "action": "scale_up",
            "status": "pending",
        }
    )
