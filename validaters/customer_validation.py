
from models.Customer_Model import Customer
from pydantic import ValidationError


def validate_customers(data)-> list[Customer]:
    valid_customers = []

    for record in data:
        try:
            customer = Customer(**record)
            valid_customers.append(customer)

        except ValidationError as e:
            print("Validation Error: " + e.json())

    return valid_customers
