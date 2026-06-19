from pydantic import BaseModel,Field,EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class TicketStatusType(Enum):
    New = "new"
    OPEN = "open"
    PENDING = "pending"
    HOLD = "hold"
    SOLVED = "solved"
    CLOSED = "closed"

class TicketPriorityType(Enum):
    Low = "low"
    Normal = "normal"
    High = "high"
    Urgent = "urgent"

class TicketType(Enum):
    PROBLEM = "problem"
    INCIDENT = "incident"
    QUESTION = "question"
    TASK = "task"

class ZenDeskUsers(BaseModel):
    id : str = Field(alias="id")
    email : Optional[EmailStr] = None
    name : str
    phone : Optional[int] = None
    role : Optional[str] = None
    active : bool = Field(default=True)
    created_at : datetime
    updated_at : datetime



class CoreZendeskTicketModel(BaseModel):
    ticket_id: int = Field(alias="id")
    url: Optional[str] = None
    description : Optional[str] = None
    title = Optional[str] = None
    requester_id: int  
    assignee_id: Optional[int] = None  
    
    # Status & Categorization
    subject: Optional[str] = None
    status: TicketStatusType  
    priority: Optional[TicketPriorityType] = None  
    type: Optional[TicketType] = None  
    
    created_at: datetime
    updated_at: datetime