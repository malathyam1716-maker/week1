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
    metadata: Dict[str, Any] = Field(default_factory=dict)
    invoice_prefix: Optional[str] = None
    created_unix: int = Field(alias="created")


class StripeChargeModel(BaseModel):
    charge_id: str = Field(alias="id")
    object_type: str = Field(default="charge", alias="object")
    customer_id: Optional[str] = Field(default=None, alias="customer")
    invoice_id: Optional[str] = Field(default=None, alias="invoice")
    payment_intent_id: Optional[str] = Field(default=None, alias="payment_intent")
    balance_transaction_id: Optional[str] = Field(default=None, alias="balance_transaction")
    amount_in_cents: int = Field(alias="amount")
    currency: str
    paid: bool
    status: str
    payment_method: Optional[str] = None
    failure_code: Optional[str] = None
    failure_message: Optional[str] = None
    receipt_email: Optional[str] = None
    receipt_number: Optional[str] = None
    receipt_url: Optional[HttpUrl] = None
    created_unix: int = Field(alias="created")
