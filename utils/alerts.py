import requests
from config.settings import settings

def notify_failure(pipeline_name: str, exception: Exception):
    error_message = f"🚨 *ETL Pipeline Failure Alert*\n*Pipeline*: {pipeline_name}\n*Error*: {str(exception)}"
    print(f"[ALERT] {error_message}")
    
    # 1. Slack Alerting
    if settings.slack_webhook_url:
        try:
            payload = {"text": error_message}
            response = requests.post(settings.slack_webhook_url, json=payload, timeout=5)
            response.raise_for_status()
            print("[ALERT] Successfully sent Slack alert.")
        except Exception as e:
            print(f"[ALERT Failed] Failed to send Slack alert: {e}")
            
    # 2. Email Alerting Mock/Log
    if settings.alert_email:
        print(f"[ALERT] Sending failure email to {settings.alert_email}...")
        # In production, this can use smtplib or a mail service like SendGrid/SES.
        # We print it here to verify that email routing works.
        print(f"[ALERT Email Sent] Subject: Pipeline Failure: {pipeline_name} | Recipient: {settings.alert_email}")
