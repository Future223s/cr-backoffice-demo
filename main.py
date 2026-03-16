from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from limiter import limiter, ENVIRONMENT, DEFAULT_RATE_LIMIT

from hr.router import router as hr_router
from finance.router import router as finance_router
from infra.router import router as infra_router
from data_analytics.router import router as data_router
from helpdesk.router import router as helpdesk_router
from procurement.router import router as procurement_router

from deps import error, success


app = FastAPI(
    title="CR Backoffice APIs",
    description="Mock Back-Office APIs for Agentic Runtime Demo",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content=error("Rate limit exceeded"),
    )


app.include_router(hr_router, prefix="/hr", tags=["HR"])
app.include_router(finance_router, prefix="/finance", tags=["Finance"])
app.include_router(infra_router, prefix="/infra", tags=["Infrastructure"])
app.include_router(data_router, prefix="/data", tags=["Data Analytics"])
app.include_router(helpdesk_router, prefix="/helpdesk", tags=["Helpdesk"])
app.include_router(procurement_router, prefix="/procurement", tags=["Procurement"])


@app.get("/", tags=["Health"])
@limiter.limit("30/minute")
def root(request: Request):
    return success(
        {
            "service": "CR Backoffice APIs",
            "environment": ENVIRONMENT,
            "default_rate_limit": DEFAULT_RATE_LIMIT,
            "status": "running",
        }
    )