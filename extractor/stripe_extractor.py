from stripe import StripeClient


client = StripeClient("<stripe_api_key>")
charges = client.v1.charges.list({"limit": 3})

print(charges ) # Uses the same request specific API Key.