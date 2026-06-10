from stripe import StripeClient
from config.settings import settings

client = StripeClient(settings.stripe_api_key)
charges = client.v1.charges.list({"limit": 3})

print(charges ) # Uses the same request specific API Key.