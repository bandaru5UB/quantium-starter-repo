import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
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

# Dash app setup
app = dash.Dash(__name__)

# Visualization 1: Total sales by product
fig1 = px.bar(df.groupby('product')['sales'].sum().reset_index(),
              x='product', y='sales', title='Total Sales by Product')

# Visualization 2: Sales over time (by date)
fig2 = px.line(df.groupby('date')['sales'].sum().reset_index(),
               x='date', y='sales', title='Total Sales Over Time')

# Visualization 3: Sales by region and product
fig3 = px.bar(df.groupby(['region', 'product'])['sales'].sum().reset_index(),
              x='region', y='sales', color='product', barmode='group',
              title='Sales by Region and Product')

app.layout = html.Div([
    html.H1('Quantium Sales Data Dashboard'),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3)
])

if __name__ == '__main__':
    app.run(debug=True)
