from pydantic import BaseModel
from typing import List, Optional


class Ticket(BaseModel):
    ticket_id: str
    user_id: str
    title: str
    status: str  # open / in_progress / waiting_on_user / resolved
    priority: str  # P1 / P2 / P3 / P4
    created_at: str
    last_updated_at: str
    category: str  # access / payments / device / network / software
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


class KBArticle(BaseModel):
    article_id: str
    title: str
    tags: List[str]
    last_updated_at: str
    summary: str


class CreateTicketRequest(BaseModel):
    user_id: str
    title: str
    category: str
    description: str
    priority: str  # P1 / P2 / P3 / P4


class CreateTicketResponse(BaseModel):
    ticket_id: str
    status: str