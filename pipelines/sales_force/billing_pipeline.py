from config.settings import settings
from integrations.sales_force import *
from pipelines.base_pipeline import BasePipeline
from utils.validator import validator

class BillingPipeline(BasePipeline):

    def extract(self):
        extractor = SalesForceExtractor(base_url=settings.salesforce_endpoint, access_token=settings.salesforce_access_token)
        return extractor.extract(BILLING_QUERY)

    def validate(self, data):
        return validator(
            data,
            SalesForceBilling
        )

    def transform(self, data):
        return data

    def load(self, data):
        print(f"Loaded {len(data)} billing records")