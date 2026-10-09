import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from quant_engine import fetch_advanced_data, run_quant_forecast
from backtester import run_backtest
from swarm_agents import run_aegis_swarm
import datetime

st.set_page_config(page_title="Aegis: Autonomous Wealth Swarm", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for next-level UI
st.markdown("""
<style>
    .big-font { font-size: 24px !important; font-weight: bold; color: #4CAF50;}
    .agent-box { background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #00BFFF;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Aegis: Autonomous Wealth Swarm")
st.markdown("An institutional-grade **Multi-Agent Hedge Fund Simulator**. Features real-time technical analysis, Gradient Boosting forecasts, Sentiment Scraping, and Portfolio Backtesting.")

# Sidebar
st.sidebar.header("Command Center")
ticker = st.sidebar.text_input("Target Asset (Ticker)", value="NVDA").upper()
st.sidebar.markdown("---")
st.sidebar.info("Set `GEMINI_API_KEY` in environment for live GenAI Swarm inference. Fallback mock engine active otherwise.")

if st.sidebar.button("Deploy Swarm", type="primary"):
    with st.spinner("Fetching Institutional Data & Computing Technicals..."):
        df = fetch_advanced_data(ticker, "2y")
        
    if df is None or df.empty:
        st.error(f"Insufficient data for {ticker}.")
    else:
        current_price = df['Close'].iloc[-1]
        
        # Tabs for deep analysis
        tab1, tab2, tab3 = st.tabs(["📊 Live Swarm Analysis", "📈 Account Growth Backtest", "🧠 Swarm Brain Logs"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"${current_price:.2f}")
            col2.metric("RSI (14)", f"{df['RSI'].iloc[-1]:.1f}")
            col3.metric("MACD", f"{df['MACD'].iloc[-1]:.2f}")
            
            with st.spinner("Training Gradient Boosting Quant Model..."):
                forecast_prices, ml_confidence = run_quant_forecast(df)
            
            st.markdown("### Advanced Candlestick & ML Forecast Overlay")
            fig = go.Figure()
            # Candlestick
            fig.add_trace(go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Market Data'))
            # Bollinger Bands
            fig.add_trace(go.Scatter(x=df['Date'], y=df['BB_High'], line=dict(color='gray', width=1, dash='dot'), name='BB Upper'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['BB_Low'], line=dict(color='gray', width=1, dash='dot'), name='BB Lower'))
            
            # Forecast
            last_date = df['Date'].iloc[-1]
            future_dates = [last_date + datetime.timedelta(days=i) for i in range(1, 8)]
            fig.add_trace(go.Scatter(x=[last_date] + future_dates, y=[current_price] + forecast_prices, mode='lines+markers', name='Quant Forecast (7D)', line=dict(color='#00ff00', width=3)))
            
            fig.update_layout(height=500, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=30,b=0))
            st.plotly_chart(fig, use_container_width=True)
            
            with st.spinner("Initializing AI Swarm & Scraping News..."):
                swarm_result = run_aegis_swarm(ticker, current_price, forecast_prices, ml_confidence, df)
            
            st.markdown("### ⚡ Execution Engine Consensus")
            exec_data = swarm_result['execution']
            decision_color = "green" if exec_data['decision'] == "BUY" else "red" if exec_data['decision'] == "SELL" else "gray"
            st.markdown(f"<p style='font-size: 30px; font-weight: bold; color: {decision_color};'>ACTION: {exec_data['decision']} (Confidence: {exec_data['confidence_score']}%)</p>", unsafe_allow_html=True)
            st.info(f"**Reasoning:** {exec_data['reasoning']}")

        with tab2:
            st.markdown("### 💰 AI Portfolio Growth Simulator ($10k Start)")
            st.markdown("If you gave this Swarm $10,000 two years ago, how would it perform against Buy & Hold?")
            
            with st.spinner("Running historical backtest..."):
                bt_df, bt_metrics = run_backtest(df)
            
            if bt_df is not None:
                mcol1, mcol2, mcol3, mcol4 = st.columns(4)
                mcol1.metric("Buy & Hold Return", bt_metrics['BH_Total_Return'])
                mcol2.metric("AI Swarm Return", bt_metrics['AI_Total_Return'], delta=bt_metrics['Alpha_Generated'])
                mcol3.metric("Final Account Value", bt_metrics['AI_Final_Value'])
                mcol4.metric("Alpha Generated", bt_metrics['Alpha_Generated'])
                
                fig_bt = go.Figure()
                fig_bt.add_trace(go.Scatter(x=bt_df['Date'], y=bt_df['Buy_Hold_Portfolio'], mode='lines', name='Buy & Hold S&P 500', line=dict(color='gray')))
                fig_bt.add_trace(go.Scatter(x=bt_df['Date'], y=bt_df['AI_Portfolio'], mode='lines', name='Aegis Swarm Managed', line=dict(color='#00BFFF', width=2)))
                fig_bt.update_layout(height=400, template="plotly_dark", title="Equity Curve")
                st.plotly_chart(fig_bt, use_container_width=True)
            else:
                st.warning("Not enough data to run a 2-year backtest.")
                
        with tab3:
            st.markdown("### 🧠 Swarm Neural Logs")
            for log in swarm_result['logs']:
                st.markdown(f"<div class='agent-box'><strong>{log['agent']}</strong><br>{log['content']}</div>", unsafe_allow_html=True)
