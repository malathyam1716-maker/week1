from config.settings import settings
from integrations.sales_force import ACCOUNT_QUERY
from integrations.sales_force import SalesForce
from integrations.sales_force import Sales_Force_Account


def process_sales_force():
    sales = SalesForce(base_url=settings.salesforce_endpoint, access_token=settings.salesforce_access_token)  
    raw_data = sales.extract(ACCOUNT_QUERY)
    validated_accounts = sales.validate(raw_data, Sales_Force_Account)
    return validated_accounts