from pipelines.sales_force.account_pipeline import AccountPipeline
from pipelines.sales_force.billing_pipeline import BillingPipeline

def main():

    # AccountPipeline().run()
    BillingPipeline().run()

if __name__ == "__main__":
    main()