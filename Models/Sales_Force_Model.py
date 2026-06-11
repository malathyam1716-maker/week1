from pydantic.main import BaseModel
import datetime

class Sales_Force_Account(BaseModel):
    id: int
    name: str
    type : str
    account_number : int
    industry : str
    revenue : int
    rating : str
    employees : int
    website : str
    ownership : str
    created_date: datetime
    updated_date: datetime

class Sales_Force_Billing(BaseModel):
    id: int
    first_name: str
    last_name: str
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

