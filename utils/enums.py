from enum import Enum


class StripeServiceEnum(Enum):
    customers = "customers" 
    charges = "charges"

class SalesForceServiceEnum(Enum):
    accounts = "account"
    contacts = "contact"

class ZenDeskServiceEnum(Enum):
    users = "users"
    