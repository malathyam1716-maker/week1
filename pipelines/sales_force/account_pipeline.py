from pipelines.base_pipeline import BasePipeline
from integrations.sales_force import *
from config.settings import settings
from utils.validator import validator
from abc import ABC,abstractmethod


class AccountPipeline(BasePipeline) :

    def extract(self):
        extractor = SalesForceExtractor(base_url=settings.salesforce_endpoint, access_token=settings.salesforce_access_token)
        return extractor.extract(ACCOUNT_QUERY)

    def validate(self, data):
        return validator(
            data,
            SalesForceAccount
        )

    def transform(self, data):
        return data

    def load(self, data):
        print(f"Loaded {len(data)} accounts")

