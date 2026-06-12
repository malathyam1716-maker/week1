from pydantic.main import BaseModel
from datetime import datetime
from typing import Union,Optional

class Sales_Force_Account(BaseModel):
    Id: int | str
    Name: str
    Type: Optional[str] = None
    AccountNumber: Optional[int | str] = None
    Industry: Optional[str] = None
    AnnualRevenue: Optional[int |str]= None
    Rating: Optional[int |str]= None
    NumberOfEmployees: Optional[int] = None
    Website: Optional[str] = None    
    Ownership: Optional[str] = None
    CreatedDate: datetime
    LastModifiedDate: datetime

class Sales_Force_Billing(BaseModel):
    Id: int | str
    FirstName: str
    LastName: str
    email: str
    phone: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    account_number: int
    created_date: datetime
    updated_date: datetime
    account_id : int

