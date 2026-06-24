from config.settings import settings
from pipeline.pipelines import get_salesforce_account_pipeline, get_stripe_customer_pipeline, get_zendesk_user_pipeline, get_salesforce_contact_pipeline,get_stripe_charge_pipeline
from loaders.s3_loader import S3Loader
from loaders.db_loader import DBLoader


def main():
    # 1. Initialize Shared Loaders (Dependencies)
    s3_loader = S3Loader(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        bucket_name=settings.aws_s3_bucket_name
    )
    console_loader = DBLoader()

    # 2. Build Pipelines
    # sf_account_pipeline = get_salesforce_account_pipeline(s3_loader, console_loader)
    # sf_contact_pipeline = get_salesforce_contact_pipeline(s3_loader, console_loader)
    # stripe_customer_pipeline = get_stripe_customer_pipeline(s3_loader, console_loader)
    stripe_charge_pipeline = get_stripe_charge_pipeline(s3_loader, console_loader)
    # zendesk_user_pipeline = get_zendesk_user_pipeline(s3_loader, console_loader)

    # 3. Run Pipelines
    # sf_account_pipeline.run()
    # sf_contact_pipeline.run()
    # stripe_customer_pipeline.run()
    stripe_charge_pipeline.run()
    # zendesk_user_pipeline.run()

if __name__ == "__main__":
    main()
