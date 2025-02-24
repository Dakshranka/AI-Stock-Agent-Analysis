import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import os

def fetch_stock_data(ticker):
    """Fetch historical stock data using Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="1mo")  # Get last 1 month data
        return stock_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

def plot_stock_trend(ticker):
    """Generate a stock price trend chart using Plotly and save as an image."""
    stock_data = fetch_stock_data(ticker)
    if stock_data.empty:
        return None

    # 📊 Create interactive plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=stock_data.index, 
        y=stock_data["Close"], 
        mode="lines",
        name="Close Price",
        line=dict(color='royalblue', width=2)
    ))

    # 🖼️ Save Plot
    chart_filename = f"{ticker}_stock_chart.png"
    fig.write_image(chart_filename)
    return chart_filename
