from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import os
import traceback
from deps import success
from limiter import limiter

from .models import PurchaseOrderRequest
from .stub_data import BUDGETS, SPEND_REPORTS, PENDING_INVOICES, COST_CENTERS
from .prompt import INSTRUCTIONS, TOOLS
from agent.agent import Agent

router = APIRouter()

agent = Agent(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=f"http://127.0.0.1:{os.getenv('PORT', '8000')}",
    model_name=os.getenv("GEMINI_MODEL_DEV", "gemini-2.5-flash-lite"),
    temperature=os.getenv("TEMPERATURE_DEV", 0.2),
    instructions=INSTRUCTIONS,
    tools_prefix="/finance",
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


@router.get("/budget/{department}/{fy}")
@limiter.limit("50/minute")
def get_budget(department: str, fy: int, request: Request):
    budget = BUDGETS.get((department, fy))
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return success(budget)


@router.get("/spend-report")
@limiter.limit("40/minute")
def get_spend_report(department: str, request: Request):
    report = SPEND_REPORTS.get(department)
    if not report:
        raise HTTPException(status_code=404, detail="Spend report not found")
    return success(report)


@router.get("/invoices/pending")
@limiter.limit("30/minute")
def get_pending_invoices(request: Request):
    return success(PENDING_INVOICES)


@router.get("/cost-centers")
@limiter.limit("30/minute")
def get_cost_centers(request: Request):
    return success(COST_CENTERS)


@router.post("/purchase-order")
@limiter.limit("15/minute")
def raise_purchase_order(payload: PurchaseOrderRequest, request: Request):
    return success({"po_id": "po_2025_118", "status": "pending"})
