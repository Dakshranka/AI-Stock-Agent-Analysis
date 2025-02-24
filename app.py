import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import speech_recognition as sr
from autogen.agentchat import UserProxyAgent
from langchain.chat_models import ChatOpenAI

# 🔹 Disable Docker for AutoGen
user_agent = UserProxyAgent("UserAgent", human_input_mode="ALWAYS", code_execution_config={"use_docker": False})

# 🎙 Speech Recognition Setup
recognizer = sr.Recognizer()

def voice_input():
    """Capture voice input and convert to text."""
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand speech"
        except sr.RequestError:
            return "Error with Speech Recognition service"

# 🔹 Streamlit UI
st.set_page_config(page_title="Stock Analysis & Prediction", layout="wide")
st.title("📈 AI Stock Market Analysis & Prediction with Voice & Multi-Agent System")
st.sidebar.header("Stock Selection")

# 🎙 Voice Command Button
if st.sidebar.button("🎙 Use Voice Input"):
    spoken_text = voice_input()
    st.sidebar.write(f"You said: {spoken_text}")
    ticker = spoken_text.upper().strip()
else:
    ticker = st.sidebar.text_input("Enter Stock Symbol", "RELIANCE.NS").upper().strip()

# 🔹 News API Key (Replace with your own key)
NEWS_API_KEY = "3be1d0d340fd4ca0a087b7f1f60ee4bb"

class StockFetcherAgent:
    """Agent responsible for fetching stock data."""
    def fetch_stock_data(self, ticker):
        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo")
        return hist if not hist.empty else None
    
    def fetch_stock_news(self, ticker):
        url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        return response.json().get("articles", [])[:5] if response.status_code == 200 else []

class StockAnalyzerAgent:
    """Agent responsible for analyzing stock trends."""
    def analyze_data(self, stock_data):
        df = stock_data.copy()
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['RSI'] = 100 - (100 / (1 + (df['Close'].diff().where(df['Close'].diff() > 0, 0)
                                       .rolling(14).mean() / df['Close'].diff().where(df['Close'].diff() < 0, 0)
                                       .rolling(14).mean())))
        return df

fetcher_agent = StockFetcherAgent()
analyzer_agent = StockAnalyzerAgent()

def handle_stock_request(ticker):
    stock_data = fetcher_agent.fetch_stock_data(ticker)
    if stock_data is None:
        return None, None
    analyzed_data = analyzer_agent.analyze_data(stock_data)
    return stock_data, analyzed_data

def plot_stock_trend(stock_data, ticker):
    """Generate stock price trend chart using Plotly."""
    if stock_data is None or stock_data.empty:
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name="Closing Price", line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["SMA_20"], mode="lines", name="20-day SMA", line=dict(color='orange')))
    fig.update_layout(title=f"{ticker} Stock Price Trend", xaxis_title="Date", yaxis_title="Price (INR)" if ".NS" in ticker or ".BO" in ticker else "Price (USD)")
    
    return fig

def predict_stock_prices(stock_data):
    """Predict future stock prices using Simple Moving Average (SMA)."""
    if stock_data is None or stock_data.empty:
        return None

    stock_data["SMA_5"] = stock_data["Close"].rolling(window=5).mean()
    
    last_price = stock_data["Close"].iloc[-1]
    sma_5 = stock_data["SMA_5"].iloc[-1]

    future_dates = [datetime.today() + timedelta(days=i) for i in range(1, 6)]
    future_prices = [sma_5 + (i * (sma_5 - last_price) / 5) for i in range(1, 6)]

    return pd.DataFrame({"Date": future_dates, "Predicted Price": future_prices})

def fetch_stock_news(ticker):
    """Fetch latest stock-related news from NewsAPI."""
    return fetcher_agent.fetch_stock_news(ticker)

# 🔹 Fetch Stock Data
stock_data, analyzed_data = handle_stock_request(ticker)

if stock_data is None or stock_data.empty:
    st.error("Invalid ticker symbol or no data available.")
else:
    # 🔹 Show Stock Data
    st.subheader(f"Stock Data: {ticker}")
    st.dataframe(stock_data.tail(10))  # Show last 10 days

    # 🔹 Show Stock Trend Chart
    chart_fig = plot_stock_trend(analyzed_data, ticker)
    if chart_fig:
        st.plotly_chart(chart_fig)

    # 🔹 Predict Stock Prices
    predictions = predict_stock_prices(stock_data)
    if predictions is not None:
        st.subheader("📊 Predicted Prices for Next 5 Days")
        st.dataframe(predictions)

    # 🔹 Fetch and Display Stock News
    stock_news = fetch_stock_news(ticker)
    if stock_news:
        st.subheader(f"📰 Latest News on {ticker}")
        for article in stock_news:
            st.markdown(f"🔹 [{article['title']}]({article['url']})")
    else:
        st.warning("No news articles found.")
