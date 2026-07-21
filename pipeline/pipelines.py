from integrations.salesforce.extractor import SalesForceExtractor
from integrations.salesforce.transformer import SalesForceTransformer
from integrations.salesforce import SalesForceAccount, SalesForceContact, ACCOUNT_QUERY, CONTACT_QUERY

from integrations.stripe.extractor import StripeExtractor
from integrations.stripe.transformer import StripeTransformer 
from integrations.stripe.models import StripeCustomerModel, StripeChargeModel

from integrations.zendesk.extractor import ZenDeskExtractor
from integrations.zendesk.transformer import ZenDeskTransformer
from integrations.zendesk.models import ZenDeskUsers

from pipeline.base_pipeline import BasePipeline
from config.settings import settings
from utils.enums import StripeServiceEnum, SalesForceServiceEnum


def get_salesforce_account_pipeline(raw_loader, final_loader):
    return BasePipeline(
        name="SalesForceAccountPipeline",
        model=SalesForceAccount,
        extractor=SalesForceExtractor(settings.salesforce_endpoint, settings.salesforce_access_token, ACCOUNT_QUERY),
        transformer=SalesForceTransformer(record_type=SalesForceServiceEnum.accounts),
        raw_loader=raw_loader,
        final_loader=final_loader
    )

def get_salesforce_contact_pipeline(raw_loader,final_loader):
    return BasePipeline(
        name="SalesForceContactPipeline",
        model=SalesForceContact,
        extractor=SalesForceExtractor(settings.salesforce_endpoint, settings.salesforce_access_token, CONTACT_QUERY),
        transformer=SalesForceTransformer(record_type=SalesForceServiceEnum.contacts),
        raw_loader=raw_loader,
        final_loader=final_loader
    )

def get_stripe_customer_pipeline(raw_loader, final_loader):
    return BasePipeline(
        name="StripeCustomerPipeline",
        model=StripeCustomerModel,
        extractor=StripeExtractor(settings.stripe_api_key, StripeServiceEnum.customers),
        transformer=StripeTransformer(record_type=StripeServiceEnum.customers),
        raw_loader=raw_loader,
        final_loader=final_loader
    )

def get_stripe_charge_pipeline(raw_loader, final_loader):
    return BasePipeline(
        name="StripeChargePipeline",
        model=StripeChargeModel,
        extractor=StripeExtractor(settings.stripe_api_key, StripeServiceEnum.charges),
        transformer=StripeTransformer(record_type=StripeServiceEnum.charges),
        raw_loader=raw_loader,
        final_loader=final_loader
    )

def get_zendesk_user_pipeline(raw_loader, final_loader):
    return BasePipeline(
        name="ZenDeskUserPipeline",
        model=ZenDeskUsers,
        extractor=ZenDeskExtractor(service_type="users"),
        transformer=ZenDeskTransformer(),
        raw_loader=raw_loader,
        final_loader=final_loader
    )
