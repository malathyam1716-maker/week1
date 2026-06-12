from pipelines.sales_force_pipeline import process_sales_force

def main():
    sales_force_data = process_sales_force()
    print(sales_force_data)

if __name__ == "__main__":
    main()