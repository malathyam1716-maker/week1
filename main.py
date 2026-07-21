import sys
from config.settings import settings
from pipeline.pipelines import (
    get_salesforce_account_pipeline,
    get_stripe_customer_pipeline,
    get_zendesk_user_pipeline,
    get_salesforce_contact_pipeline,
    get_stripe_charge_pipeline
)
from loaders.s3_loader import S3Loader
from loaders.db_loader import DBLoader
from utils.alerts import notify_failure

def main():
    print("--- Starting Enterprise ETL Pipeline & Data Warehouse Synchronizer ---")
    
    # 1. Initialize Shared Loaders (Dependencies)
    s3_loader = S3Loader(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        bucket_name=settings.aws_s3_bucket_name
    )
    
    db_loader = DBLoader()

    # 2. Build Pipelines
    pipelines = {
        "Salesforce Accounts": get_salesforce_account_pipeline(s3_loader, db_loader),
        "Salesforce Contacts": get_salesforce_contact_pipeline(s3_loader, db_loader),
        "Stripe Customers": get_stripe_customer_pipeline(s3_loader, db_loader),
        "Stripe Charges": get_stripe_charge_pipeline(s3_loader, db_loader),
        "Zendesk Users": get_zendesk_user_pipeline(s3_loader, db_loader)
    }

    # 3. Run Pipelines
    failed_pipelines = []
    
    for name, pipeline in pipelines.items():
        print(f"\n[Executing] {name} Pipeline...")
        try:
            pipeline.run()
            print(f"[Success] {name} Pipeline completed successfully.")
        except Exception as e:
            error_msg = f"{name} Pipeline failed: {e}"
            print(f"[Error] {error_msg}")
            notify_failure(name, e)
            failed_pipelines.append(name)

    print("\n--- ETL Execution Summary ---")
    if failed_pipelines:
        print(f"FAILED Pipelines: {', '.join(failed_pipelines)}")
        sys.exit(1)
    else:
        print("All pipelines completed successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
