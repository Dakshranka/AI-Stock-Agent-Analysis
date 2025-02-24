import autogen
from stock_tool import fetch_stock_data, plot_stock_trend  # Import the tool

# Initialize the agent
stock_agent = autogen.ConversableAgent(
    name="StockAgent",
    system_message="I can fetch stock prices and generate stock charts for you."
)

def get_stock_info(ticker: str) -> str:
    """Fetch stock information and return as text."""
    stock_data = fetch_stock_data(ticker)  # Use stock_tool function
    
    if stock_data is None or stock_data.empty:
        return f"Invalid ticker: {ticker}. Please enter a valid stock symbol."
    
    return stock_data.tail(5).to_string()

def get_stock_chart(ticker: str) -> str:
    """Generate stock trend visualization and return image file path."""
    chart_path = plot_stock_trend(ticker)  # Use stock_tool function
    return chart_path if chart_path else None

# ✅ Correct function registration (Dictionary Format)
stock_agent.register_function({
    "get_stock_info": get_stock_info,
    "get_stock_chart": get_stock_chart
})

# Function to interact with the agent
def query_stock_agent(ticker):
    """Query the stock agent to get stock data and chart."""
    stock_data_response = get_stock_info(ticker)
    stock_chart_response = get_stock_chart(ticker)
    return stock_data_response, stock_chart_response
