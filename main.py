from pipelines.sales_force_pipeline import process_salesForce_account,process_salesForce_billing

def main():
    # Data Extraction and Validation for Sales Force Accounts
    # sales_force_data = process_salesForce_account()
    # print(sales_force_data)

    # Data Extraction and Validation for Sales Force Billing
    sales_force_billing_data = process_salesForce_billing()
    print(sales_force_billing_data)

if __name__ == "__main__":
    main()