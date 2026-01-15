import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import os

# Load data
df = pd.read_csv("data/sales.csv")
df["Revenue"] = df["Quantity"] * df["Price"]
df["Date"] = pd.to_datetime(df["Date"])

# KPIs
total_revenue = df["Revenue"].sum()
total_quantity = df["Quantity"].sum()

# Charts
sales_trend = px.line(
    df.groupby("Date")["Revenue"].sum().reset_index(),
    x="Date",
    y="Revenue",
    title="Sales Trend Over Time"
)

region_sales = px.pie(
    df.groupby("Region")["Revenue"].sum().reset_index(),
    names="Region",
    values="Revenue",
    title="Revenue by Region"
)

product_sales = px.bar(
    df.groupby("Product")["Revenue"].sum().reset_index(),
    x="Product",
    y="Revenue",
    title="Revenue by Product"
)

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H3("Total Revenue"),
            html.H4(f"₹ {total_revenue:,}")
        ], style={"width": "48%", "display": "inline-block"}),

        html.Div([
            html.H3("Total Quantity Sold"),
            html.H4(f"{total_quantity:,}")
        ], style={"width": "48%", "display": "inline-block"})
    ]),

    dcc.Graph(figure=sales_trend),
    dcc.Graph(figure=region_sales),
    dcc.Graph(figure=product_sales)
])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)), debug=False)

