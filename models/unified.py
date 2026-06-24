from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UnifiedCustomer(BaseModel):
    id: str
    source_system: str
    name: str
    email: Optional[EmailStr | str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UnifiedTransaction(BaseModel):
    id: str
    source_system: str
    customer_id: str
    amount: float
    currency: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
