from integrations.salesforce.extractor import SalesForceExtractor
from integrations.salesforce.transformer import SalesForceTransformer
from integrations.salesforce import SalesForceAccount, SalesForceBilling, ACCOUNT_QUERY, BILLING_QUERY

from integrations.stripe.extractor import StripeExtractor, ServiceEnum
from integrations.stripe.transformer import StripeTransformer 
from integrations.stripe.models import StripeCustomerModel, StripeChargeModel

from integrations.zendesk.extractor import ZenDeskExtractor
from integrations.zendesk.transformer import ZenDeskTransformer
from integrations.zendesk.models import ZenDeskUsers
from pipelines.base_pipeline import BasePipeline
from config.settings import settings


def get_salesforce_account_pipeline(raw_loader, final_loader):
    return BasePipeline(
        name="SalesForceAccountPipeline",
        model=SalesForceAccount,
        extractor=SalesForceExtractor(settings.salesforce_endpoint, settings.salesforce_access_token, ACCOUNT_QUERY),
        transformer=SalesForceTransformer(record_type="account"),
        raw_loader=raw_loader,
        final_loader=final_loader
    )

def get_stripe_customer_pipeline(raw_loader, final_loader):
    return BasePipeline(
        name="StripeCustomerPipeline",
        model=StripeCustomerModel,
        extractor=StripeExtractor(settings.stripe_api_key, ServiceEnum.customers),
        transformer=StripeTransformer(record_type="customer"),
        raw_loader=raw_loader,
        final_loader=final_loader
    )

def get_zendesk_user_pipeline(raw_loader, final_loader):
    return BasePipeline(
        name="ZenDeskUserPipeline",
        model=ZenDeskUsers,
        extractor=ZenDeskExtractor(settings.zendesk_endpoint, settings.zendesk_access_token, "users"),
        transformer=ZenDeskTransformer(),
        raw_loader=raw_loader,
        final_loader=final_loader
    )
