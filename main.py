from validaters.customer_validation import validate_customers

# Sample API Data
sample_data = [
    {
        "id": 1,
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com"
    },
    {
        "id": 2,
        "firstName": "Alice",
        "lastName": "Smith",
        "email": "alice@example.com"
    }
]


customers = validate_customers(sample_data)

print("\nValidated Customers")

for customer in customers:
    print(customer)
