from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from config.settings import settings
from loaders.s3_loader import S3Loader
from loaders.db_loader import DBLoader
from pipeline.pipelines import (
    get_salesforce_account_pipeline,
    get_salesforce_contact_pipeline,
    get_stripe_customer_pipeline,
    get_stripe_charge_pipeline,
    get_zendesk_user_pipeline
)
from utils.alerts import notify_failure

default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_pipeline(pipeline_getter):
    print(f"Starting execution of pipeline: {pipeline_getter.__name__}")
    s3_loader = S3Loader(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        bucket_name=settings.aws_s3_bucket_name
    )
    db_loader = DBLoader()
    pipeline = pipeline_getter(s3_loader, db_loader)
    pipeline.run()
    print(f"Finished execution of pipeline: {pipeline_getter.__name__}")

def on_task_failure(context):
    task_instance = context.get('task_instance')
    exception = context.get('exception')
    notify_failure(task_instance.task_id, exception)

with DAG(
    'enterprise_etl_data_warehouse_sync',
    default_args=default_args,
    description='Resilient ETL sync pipeline for Salesforce, Stripe, and Zendesk APIs into Data Warehouse',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # 1. Stripe Pipelines
    run_stripe_customers = PythonOperator(
        task_id='run_stripe_customers',
        python_callable=run_pipeline,
        op_args=[get_stripe_customer_pipeline],
        on_failure_callback=on_task_failure,
    )

    run_stripe_charges = PythonOperator(
        task_id='run_stripe_charges',
        python_callable=run_pipeline,
        op_args=[get_stripe_charge_pipeline],
        on_failure_callback=on_task_failure,
    )

    # 2. Salesforce Pipelines
    run_salesforce_accounts = PythonOperator(
        task_id='run_salesforce_accounts',
        python_callable=run_pipeline,
        op_args=[get_salesforce_account_pipeline],
        on_failure_callback=on_task_failure,
    )

    run_salesforce_contacts = PythonOperator(
        task_id='run_salesforce_contacts',
        python_callable=run_pipeline,
        op_args=[get_salesforce_contact_pipeline],
        on_failure_callback=on_task_failure,
    )

    # 3. Zendesk Pipelines
    run_zendesk_users = PythonOperator(
        task_id='run_zendesk_users',
        python_callable=run_pipeline,
        op_args=[get_zendesk_user_pipeline],
        on_failure_callback=on_task_failure,
    )

    # All tasks run in parallel daily
    [
        run_stripe_customers,
        run_stripe_charges,
        run_salesforce_accounts,
        run_salesforce_contacts,
        run_zendesk_users
    ]
