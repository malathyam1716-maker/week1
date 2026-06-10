from pydantic import BaseModel,EmailStr


# Pydantic Model
class Customer(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: EmailStr


