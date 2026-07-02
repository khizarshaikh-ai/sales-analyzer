import pandas as pd
import random
from datetime import datetime, timedelta


def create_mock_data():
    products = ['Laptop Pro', 'Wireless Mouse', '4K Monitor', 'Mechanical Keyboard', 'USB-C Hub', 'Gaming Chair',
                'Webcam HD']
    categories = ['Electronics', 'Accessories', 'Electronics', 'Accessories', 'Accessories', 'Furniture', 'Electronics']
    regions = ['North', 'South', 'East', 'West']
    prod_cat = dict(zip(products, categories))

    data = []
    start_date = datetime(2026, 6, 1)

    for i in range(200):
        prod = random.choice(products)
        qty = random.randint(1, 5)
        price = round(random.uniform(15.0, 1200.0), 2)
        sales = round(qty * price, 2)
        date = start_date + timedelta(days=random.randint(0, 29))

        data.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Product': prod,
            'Category': prod_cat[prod],
            'Quantity': qty,
            'Price': price,
            'Sales': sales,
            'Region': random.choice(regions)
        })

    df = pd.DataFrame(data)
    df.to_csv('sample_sales_data.csv', index=False)
    print("Successfully generated 'sample_sales_data.csv' with 200 sample rows!")


if __name__ == "__main__":
    create_mock_data()