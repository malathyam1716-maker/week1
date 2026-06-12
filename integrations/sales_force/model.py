from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

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
    Email: Optional[EmailStr | str] = None
    Phone: Optional[int | str] = None
    MobilePhone :  Optional[str | int] = None
    BirthDate : Optional[datetime] = None
    Languages__c :  Optional[str] = None
    MailingStreet: Optional[str] = None
    City:  Optional[str] = None
    Street : Optional[str] = None
    State: Optional[str] = None
    PostalCode: Optional[int] = None
    Country: Optional[str] = None
    AccountId : str
    CreatedDate: datetime
    LastModifiedDate: datetime

