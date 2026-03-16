from datetime import datetime, timezone
from typing import Any, Generic, Optional, TypeVar, Literal
from pydantic import BaseModel

T = TypeVar("T")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class APIResponse(BaseModel, Generic[T]):
    data: Optional[T]
    status: Literal["success", "error"]
    timestamp: str
    message: Optional[str] = None


def success(data: Any) -> dict:
    return APIResponse(data=data, status="success", timestamp=now_iso()).model_dump()


def error(message: str, data: Any = None) -> dict:
    return APIResponse(data=data, status="error", timestamp=now_iso(), message=message).model_dump()