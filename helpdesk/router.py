from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import JSONResponse
import os
import traceback
from datetime import datetime

from limiter import limiter
from .models import CreateTicketRequest
from .stub_data import TICKETS_BY_USER, KB_ARTICLES
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
    tools_prefix="/helpdesk",
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


@router.get("/tickets/{user_id}")
@limiter.limit("40/minute")
def get_tickets(user_id: str, request: Request):
    tickets = TICKETS_BY_USER.get(user_id, [])
    # Returning empty list is OK (not a 404) - user might just have no open tickets
    return envelope(tickets)


@router.get("/kb/search")
@limiter.limit("30/minute")
def kb_search(q: str = Query(..., min_length=2), request: Request = None):
    query = q.strip().lower()

    results = []
    for a in KB_ARTICLES:
        haystack = " ".join([a["title"], " ".join(a["tags"]), a["summary"]]).lower()
        if query in haystack:
            results.append(a)

    return envelope(
        {
            "query": q,
            "results_count": len(results),
            "results": results,
        }
    )


@router.post("/ticket")
@limiter.limit("15/minute")
def create_ticket(payload: CreateTicketRequest, request: Request):
    # No persistence required - return a realistic stub confirmation
    return envelope(
        {
            "ticket_id": "tkt_2025_4099",
            "status": "open",
        }
    )
