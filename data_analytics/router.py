from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import os
import traceback
from deps import success
from limiter import limiter

from .models import QueryRequest
from .stub_data import KPIS, REPORTS, ANOMALIES
from .prompt import INSTRUCTIONS, TOOLS
from agent.agent import Agent

router = APIRouter()

agent = Agent(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=f"http://127.0.0.1:{os.getenv('PORT', '8000')}",
    model_name=os.getenv("GEMINI_MODEL_DEV", "gemini-2.5-flash-lite"),
    temperature=os.getenv("TEMPERATURE_DEV", 0.2),
    instructions=INSTRUCTIONS,
    tools_prefix="/data",
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


@router.get("/kpis/{department}")
@limiter.limit("40/minute")
def get_kpis(department: str, request: Request):
    kpi = KPIS.get(department)
    if not kpi:
        raise HTTPException(status_code=404, detail="Department KPIs not found")
    return success(kpi)


@router.get("/reports/{report_id}")
@limiter.limit("30/minute")
def get_report(report_id: str, request: Request):
    report = REPORTS.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return success(report)


@router.get("/anomalies")
@limiter.limit("30/minute")
def get_anomalies(request: Request):
    return success(ANOMALIES)


@router.post("/query")
@limiter.limit("10/minute")
def run_query(payload: QueryRequest, request: Request):
    q = payload.query.lower()

    if "infrastructure" in q and "budget" in q:
        result = {
            "columns": ["department", "burn_rate_pct", "risk_level"],
            "rows": [["Infrastructure", 74, "elevated"]],
        }
    elif "incident" in q or "mttr" in q:
        result = {
            "columns": ["metric", "change"],
            "rows": [["Incident Rate", "+23%"], ["MTTR", "-8%"]],
        }
    elif "cloudscale" in q:
        result = {
            "columns": ["vendor", "invoice_status", "contract_renewal_risk"],
            "rows": [["CloudScale Solutions", "awaiting_approval", "high"]],
        }
    else:
        result = {"columns": ["message"], "rows": [["No matching dataset found for query"]]}

    return success(result)
