from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class SalesForceAccount(BaseModel):
    Id: int | str
    Name: str
    Type: Optional[str] = None
    AccountNumber: Optional[int | str] = None
    Industry: Optional[str] = None
    AnnualRevenue: Optional[int | str] = None
    Rating: Optional[int | str] = None
    NumberOfEmployees: Optional[int] = None
    Website: Optional[str] = None
    Ownership: Optional[str] = None
    CreatedDate: datetime
    LastModifiedDate: datetime

class SalesForceBilling(BaseModel):
    Id: int | str
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Email: Optional[EmailStr | str] = None
    Phone: Optional[int | str] = None
    MobilePhone: Optional[str | int] = None
    BirthDate: Optional[datetime] = None
    Languages__c: Optional[str] = None
    MailingStreet: Optional[str] = None
    City: Optional[str] = None
    Street: Optional[str] = None
    State: Optional[str] = None
    PostalCode: Optional[int] = None
    Country: Optional[str] = None
    AccountId: Optional[str] = None
    CreatedDate: datetime
    LastModifiedDate: datetime
