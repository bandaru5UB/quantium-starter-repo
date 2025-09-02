import pandas as pd
import os

# Load all CSV files from the data directory
data_dir = os.path.join(os.path.dirname(__file__), 'data')
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
df_list = [pd.read_csv(os.path.join(data_dir, f)) for f in files]
df = pd.concat(df_list, ignore_index=True)

# Clean price column (remove $ and convert to float)
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)

# Add a sales column (price * quantity)
df['sales'] = df['price'] * df['quantity']

# Filter for pink morsel
pink_df = df[df['product'].str.lower() == 'pink morsel'].copy()

# Convert date column to datetime
pink_df['date'] = pd.to_datetime(pink_df['date'])

# Define price change date
price_change_date = pd.to_datetime('2021-01-15')

# Calculate total sales before and after the price change
total_sales_before = pink_df[pink_df['date'] < price_change_date]['sales'].sum()
total_sales_after = pink_df[pink_df['date'] >= price_change_date]['sales'].sum()

print(f"Total Pink Morsel sales before {price_change_date.date()}: ${total_sales_before:,.2f}")
print(f"Total Pink Morsel sales after {price_change_date.date()}: ${total_sales_after:,.2f}")

if total_sales_after > total_sales_before:
    print("Sales were higher after the price increase.")
elif total_sales_after < total_sales_before:
    print("Sales were higher before the price increase.")
else:
    print("Sales were the same before and after the price increase.")
