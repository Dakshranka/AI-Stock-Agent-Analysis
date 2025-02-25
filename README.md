## AI Stock Agent Analysis

# Overview
This project is an AI-powered stock analysis agent that provides insights into stock trends, market analysis, and forecasts. It uses various Python libraries, including yfinance for fetching stock data, matplotlib and plotly for visualization, streamlit for UI, and crewai for AI-driven task management.

# Features

- Stock Market Data Fetching: Uses yfinance to retrieve real-time stock data.
- Data Visualization: Provides interactive charts using matplotlib and plotly.
- Speech Recognition: Users can interact with the system via voice commands using speech_recognition.
- AI Agents: Implements AI-powered agents via crewai for automated analysis.
- Web Application: Built with streamlit for an interactive and user-friendly interface.

# Installation

# Prerequisites
- Ensure you have Python 3.8 or later installed on your system.
- Install Dependencies
Run the following command to install all required dependencies:

``` pip install -r requirements.txt ```

# Running the Application

To start the Streamlit app, run:

``` streamlit run app.py ```

# Troubleshooting
- Speech Recognition Timeout Error.
- If you encounter WaitTimeoutError, try:
- Increasing the timeout in recognizer.listen().
- Checking microphone permissions.
- Ensuring the microphone is not in use by other applications.
- Missing Module Errors
-- If you see module import errors (ModuleNotFoundError), ensure all dependencies are installed:

``` pip install -r requirements.txt ```

# Contributing
Feel free to open issues or submit pull requests to improve the project!

Daksh Ranka 
Emailid: rankadaksh4@gmail.com

# License

This project is licensed under the MIT License
