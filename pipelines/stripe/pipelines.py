from pipelines.base_pipeline import BasePipeline
from integrations.stripe.extractor import StripeExtractor, ServiceEnum
from integrations.stripe.models import StripeCustomerModel, StripeChargeModel
from config.settings import settings


class StripeAccountPipeline(BasePipeline):
    model = StripeCustomerModel

    def extract(self):
        return StripeExtractor(settings.stripe_api_key).extract(service_type=ServiceEnum.customers)
    
    def load_raw_data(self):
        pass

    def transform(self, data):
        return data

    def load(self, data):
        print(f"Loaded {len(data)} records")


class StripeChargePipeline(BasePipeline):
    model = StripeChargeModel

    def extract(self):
        return StripeExtractor(settings.stripe_api_key).extract(service_type=ServiceEnum.charges)
    
    def load_raw_data(self):
        pass

    def transform(self, data):
        return data

    def load(self, data):
        print(f"Loaded {len(data)} records")
