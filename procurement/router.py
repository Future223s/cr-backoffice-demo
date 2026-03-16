from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
import os
import traceback
from datetime import datetime
from typing import Optional

from limiter import limiter
from .models import RFQRequest
from .stub_data import VENDORS, EXPIRING_CONTRACTS
from .prompt import INSTRUCTIONS, TOOLS
from deps import success
from agent.agent import Agent

router = APIRouter()

agent = Agent(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=f"http://127.0.0.1:{os.getenv('PORT', '8000')}",
    model_name=os.getenv("GEMINI_MODEL_DEV", "gemini-2.5-flash-lite"),
    temperature=os.getenv("TEMPERATURE_DEV", 0.2),
    instructions=INSTRUCTIONS,
    tools_prefix="/procurement",
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


@router.get("/vendors")
@limiter.limit("30/minute")
def get_vendors(
    request: Request,
    name: Optional[str] = Query(None, description="Filter by vendor name (case-insensitive partial match)"),
    category: Optional[str] = Query(None, description="Filter by vendor category (case-insensitive)"),
    risk_tier: Optional[str] = Query(None, description="Filter by risk tier (case-insensitive)"),
    status: Optional[str] = Query(None, description="Filter by vendor status (case-insensitive)")
):
    # Start with all vendors
    filtered_vendors = VENDORS.copy()
    
    # Apply filters step by step using raw parameters
    if name:
        filtered_vendors = [
            vendor for vendor in filtered_vendors 
            if name.lower() in vendor["name"].lower()
        ]
    
    if category:
        filtered_vendors = [
            vendor for vendor in filtered_vendors 
            if vendor["category"].lower() == category.lower()
        ]
    
    if risk_tier:
        filtered_vendors = [
            vendor for vendor in filtered_vendors 
            if vendor["risk_tier"].lower() == risk_tier.lower()
        ]
    
    if status:
        filtered_vendors = [
            vendor for vendor in filtered_vendors 
            if vendor["status"].lower() == status.lower()
        ]
    
    return success(filtered_vendors)


@router.get("/contracts/expiring")
@limiter.limit("20/minute")
def get_expiring_contracts(request: Request):
    return success(EXPIRING_CONTRACTS)


@router.post("/rfq")
@limiter.limit("10/minute")
def submit_rfq(rfq: RFQRequest, request: Request):
    # No persistence required (stub confirmation only)
    return success(
        {
            "rfq_id": "rfq_2025_044",
            "status": "pending",
        }
    )
