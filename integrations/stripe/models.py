from pydantic import BaseModel, EmailStr, Field, HttpUrl
from datetime import datetime
from typing import Optional, Dict, Any


class StripeCustomerModel(BaseModel):
    customer_id: str = Field(alias="id")
    object_type: str = Field(default="customer", alias="object")
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    balance: int = 0
    currency: Optional[str] = "usd"
    created_unix: int = Field(alias="created")


class StripeChargeModel(BaseModel):
    charge_id: str = Field(alias="id")
    object_type: str = Field(default="charge", alias="object")
    customer_id: Optional[str] = Field(default=None, alias="customer")
    invoice_id: Optional[str] = Field(default=None, alias="invoice")
    amount_in_cents: int = Field(alias="amount")
    currency: str
    paid: bool
    status: str
    payment_method: Optional[str] = None
    created_unix: int = Field(alias="created")
