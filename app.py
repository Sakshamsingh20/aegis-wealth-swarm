import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from ml_model import fetch_stock_data, forecast_stock
from agents import generate_agent_debate
import datetime

st.set_page_config(page_title="FinSwarm Agentic Simulator", layout="wide")

st.title("🤖 FinSwarm: Agentic Portfolio Simulator")
st.markdown("An interactive showcase of **Machine Learning** (Time-Series Forecasting), **Generative AI** (Content Synthesis), and **Agentic Debates**.")

# Sidebar
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL").upper()
period = st.sidebar.selectbox("Historical Period", ["3mo", "6mo", "1y", "2y"], index=1)
st.sidebar.markdown("---")
st.sidebar.info("Set your GEMINI_API_KEY environment variable for real AI debates. Otherwise, it uses a fallback mock engine for demonstrations out of the box.")

if st.sidebar.button("Run Simulation"):
    with st.spinner(f"Fetching historical data for {ticker}..."):
        df = fetch_stock_data(ticker, period)
        
    if df.empty:
        st.error(f"Could not fetch data for {ticker}. Please try a valid ticker (e.g., AAPL, MSFT, TSLA).")
    else:
        st.success(f"Data for {ticker} fetched successfully!")
        current_price = df['Close'].iloc[-1]
        
        with st.spinner("Running ML Forecasting..."):
            forecast_prices = forecast_stock(df, days_to_forecast=7)
            
        # Plotting the Chart
        st.subheader(f"📈 {ticker} Market Trend & ML Forecast")
        fig = go.Figure()
        
        # Historical Data
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Historical Close', line=dict(color='blue')))
        
        # Forecast Data
        last_date = df['Date'].iloc[-1]
        future_dates = [last_date + datetime.timedelta(days=i) for i in range(1, 8)]
        
        # Connect the forecast line visually to the last known point
        plot_forecast_dates = [last_date] + future_dates
        plot_forecast_prices = [current_price] + forecast_prices
        
        fig.add_trace(go.Scatter(x=plot_forecast_dates, y=plot_forecast_prices, mode='lines+markers', name='ML Forecast (7 Days)', line=dict(color='orange', dash='dash')))
        
        fig.update_layout(height=400, template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Agentic Debate
        st.subheader("🗣️ Agentic Swarm Debate")
        st.markdown("Our AI agents analyze the ML forecast and debate the best trading strategy based on their engineered personas. *Note: Uses mock data unless GEMINI_API_KEY is set.*")
        
        with st.spinner("Agents are reviewing the ML model and debating..."):
            debate_log = generate_agent_debate(ticker, current_price, forecast_prices)
            
        for msg in debate_log:
            if "Conservative" in msg["role"]:
                st.info(f"**{msg['role']}:** {msg['content']}")
            elif "Aggressive" in msg["role"]:
                st.warning(f"**{msg['role']}:** {msg['content']}")
            else:
                st.success(f"**{msg['role']}:** {msg['content']}")

st.markdown("---")
st.caption("Built to demonstrate full-stack AI Engineering (ML + GenAI + Agentic AI).")
