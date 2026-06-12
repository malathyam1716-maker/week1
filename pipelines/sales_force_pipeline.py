from config.settings import settings
from integrations.sales_force import ACCOUNT_QUERY,BILLING_QUERY
from integrations.sales_force import SalesForce
from integrations.sales_force import Sales_Force_Account,Sales_Force_Billing


def process_salesForce_account():
    sales = SalesForce(base_url=settings.salesforce_endpoint, access_token=settings.salesforce_access_token)  
    raw_data = sales.extract(ACCOUNT_QUERY)
    validated_accounts = sales.validate(raw_data, Sales_Force_Account)
    return validated_accounts

def process_salesForce_billing():
    billing = SalesForce(base_url=settings.salesforce_endpoint, access_token=settings.salesforce_access_token)
    raw_data = billing.extract(BILLING_QUERY)
    validated_billing = billing.validate(raw_data, Sales_Force_Billing)
    return validated_billing