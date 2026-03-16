from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from deps import success
from limiter import limiter
from typing import List, Optional
import os
import traceback
import shutil
from pathlib import Path
import logging

from .models import LeaveRequest, MoveRequest
from agent.agent import Agent
from .prompt import INSTRUCTIONS, TOOLS
from .stub_data import HEADCOUNT, EMPLOYEES, OPEN_POSITIONS

router = APIRouter()
BASE_DIR = Path(os.getenv("AGENT_BASE_DIR", Path(__file__).resolve().parent)).resolve()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

agent = Agent(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=f"http://127.0.0.1:{os.getenv('PORT', '8000')}",
    model_name=os.getenv("GEMINI_MODEL_DEV", "gemini-2.5-flash-lite"),
    temperature=os.getenv("TEMPERATURE_DEV", 0.2),
    instructions=INSTRUCTIONS,
    tools_prefix="/hr",
)

def resolve_path(relative_path: str) -> Path:
    path = (BASE_DIR / relative_path).resolve()
    if not str(path).startswith(str(BASE_DIR)):
        raise HTTPException(status_code=403, detail="Path outside workspace")

    return path

@router.get("/files")
def list_files():
    logger.info(f"Exploring directory: {BASE_DIR}")
    if not BASE_DIR.exists() or not BASE_DIR.is_dir():
        raise HTTPException(status_code=500, detail=f"Base directory does not exist: {BASE_DIR}")

    files = []
    for p in BASE_DIR.rglob("*"):
        files.append(str(p.relative_to(BASE_DIR))) 

    return success({"files": files})

@router.post("/files/accept")
def accept_file(req: MoveRequest):
    src = resolve_path(req.source)
    dst = resolve_path("./accepted_resumes")

    if not src.exists():
        raise HTTPException(status_code=404, detail="Source file not found")

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(src, dst)

    return success({"status": "accepted", "from": req.source, "to": req.destination})

@router.get("/files/delete")
def delete_file(path: str = Query(..., description="Relative path of the file to delete")):
    file_path = resolve_path(path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    os.remove(file_path)
    return success({"status": "deleted"})


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
                "traceback": traceback.format_exc()
            }
        )

@router.get("/tools")
@limiter.limit("60/minute")
async def list_tools(request: Request):
    return success(TOOLS)

@router.get("/headcount")
@limiter.limit("60/minute")
def get_headcount(
    request: Request,
    departments: Optional[List[str]] = Query(None, description="Filter by department names (case-insensitive)"),
    employment_type: Optional[str] = Query(None, description="Filter by 'FTE' or 'Contractor'")
):
    headcount = 0
    
    # Convert departments list to set for efficient lookup
    dept_set = set()
    if departments:
        dept_set = set(dep.lower() for dep in departments)
    
    # Loop through headcount departments
    for dep_info in HEADCOUNT["departments"]:
        # Check if department is in the set (if departments filter is provided)
        if departments and dep_info["department"].lower() not in dept_set:
            continue
            
        # Check employment type and add appropriate count
        if employment_type:
            if employment_type.lower() == "fte":
                headcount += dep_info["fte"]
            elif employment_type.lower() == "contractor":
                headcount += dep_info["contractors"]
        else:
            headcount += dep_info["fte"] + dep_info["contractors"]
    
    return success({"headcount": headcount})


@router.get("/employees/{employee_id}")
@limiter.limit("60/minute")
def get_employee(employee_id: str, request: Request):
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return success(employee)


@router.get("/org-chart/{department}")
@limiter.limit("40/minute")
def get_org_chart(department: str, request: Request):
    dept_employees = [
        e for e in EMPLOYEES.values()
        if e["department"].lower() == department.lower()
    ]
    if not dept_employees:
        raise HTTPException(status_code=404, detail="Department not found")

    org_chart = [
        {
            "name": e["name"],
            "role": e["role"],
            "reports": [
                sub["name"]
                for sub in EMPLOYEES.values()
                if sub["manager"] == e["name"]
            ],
        }
        for e in dept_employees
    ]

    return success(org_chart)


@router.get("/open-positions")
@limiter.limit("30/minute")
def get_open_positions(
    request: Request,
    role: Optional[str] = Query(None, description="Filter by role (case-insensitive)"),
    department: Optional[str] = Query(None, description="Filter by department (case-insensitive)"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level (case-insensitive)"),
    hiring_stage: Optional[str] = Query(None, description="Filter by hiring stage (case-insensitive)"),
    min_budget: Optional[int] = Query(None, description="Minimum allocated budget (USD)"),
    max_budget: Optional[int] = Query(None, description="Maximum allocated budget (USD)"),
):
    # Start with all positions
    filtered_positions = OPEN_POSITIONS.copy()
    
    # Apply filters step by step using raw parameters
    if role:
        filtered_positions = [
            pos for pos in filtered_positions 
            if role.lower() in pos["role"].lower()
        ]
    
    if department:
        filtered_positions = [
            pos for pos in filtered_positions 
            if pos["department"].lower() == department.lower()
        ]
    
    if seniority:
        filtered_positions = [
            pos for pos in filtered_positions 
            if pos["seniority"].lower() == seniority.lower()
        ]
    
    if hiring_stage:
        filtered_positions = [
            pos for pos in filtered_positions 
            if pos["hiring_stage"].lower() == hiring_stage.lower()
        ]

    if min_budget is not None:
        filtered_positions = [
            pos for pos in filtered_positions 
            if pos["allocated_budget_usd"] >= min_budget
        ]

    if max_budget is not None:
        filtered_positions = [
            pos for pos in filtered_positions 
            if pos["allocated_budget_usd"] <= max_budget
        ]
    
    return success(filtered_positions)


@router.post("/leave/request")
@limiter.limit("20/minute")
def request_leave(payload: LeaveRequest, request: Request):
    return success({"request_id": "leave_2025_104", "status": "pending"})
