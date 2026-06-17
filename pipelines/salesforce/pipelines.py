from pipelines.base_pipeline import BasePipeline
from integrations.salesforce import SalesForceExtractor, SalesForceAccount, SalesForceBilling, ACCOUNT_QUERY, BILLING_QUERY
from config.settings import settings


class SalesForceAccountPipeline(BasePipeline):
    model = SalesForceAccount

    def extract(self):
        return SalesForceExtractor(base_url=settings.salesforce_endpoint, access_token=settings.salesforce_access_token).extract(ACCOUNT_QUERY)

    def transform(self, data):
        return data

    def load(self, data):
        print(f"Loaded {len(data)} salesforce accounts")


class SalesForceBillingPipeline(BasePipeline):
    model = SalesForceBilling

    def extract(self):
        return SalesForceExtractor(base_url=settings.salesforce_endpoint, access_token=settings.salesforce_access_token).extract(BILLING_QUERY)

    def transform(self, data):
        return data

    def load(self, data):
        print(f"Loaded {len(data)} salesforce billing records")
