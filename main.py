from pipelines.salesforce.pipelines import SalesForceAccountPipeline, SalesForceBillingPipeline
from pipelines.stripe.pipelines import StripeAccountPipeline, StripeChargePipeline


def main():
    StripeAccountPipeline().run()
    # StripeChargePipeline().run()
    # SalesForceAccountPipeline().run()
    # SalesForceBillingPipeline().run()

if __name__ == "__main__":
    main()
