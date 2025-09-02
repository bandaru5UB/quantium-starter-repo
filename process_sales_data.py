import pandas as pd
import os

# Load all CSV files from the data directory
data_dir = os.path.join(os.path.dirname(__file__), 'data')
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
df_list = [pd.read_csv(os.path.join(data_dir, f)) for f in files]
df = pd.concat(df_list, ignore_index=True)

# Clean price column (remove $ and convert to float)
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)

# Filter for pink morsel only
pink_df = df[df['product'].str.lower() == 'pink morsel'].copy()

# Add a sales column (price * quantity)
pink_df['sales'] = pink_df['price'] * pink_df['quantity']

# Select only the required columns
output_df = pink_df[['sales', 'date', 'region']]

# Save to CSV
output_df.to_csv('formatted_sales_data.csv', index=False)
print('Formatted sales data saved to formatted_sales_data.csv')
