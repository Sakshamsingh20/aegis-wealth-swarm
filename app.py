import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import yfinance as yf
from quant_engine import fetch_advanced_data, run_quant_forecast, calculate_pivot_points
from backtester import run_backtest
from swarm_agents import run_aegis_swarm

st.set_page_config(page_title="Aegis Pro Terminal", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Premium Dark Mode Terminal CSS */
    .metric-card { background-color: #1E1E1E; padding: 20px; border-radius: 12px; border: 1px solid #333; box-shadow: 0px 4px 6px rgba(0,0,0,0.5); color: white;}
    .ipo-card { background-color: #1E1E1E; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-bottom: 15px;}
    .ipo-card h4 { color: #00BFFF; margin-top: 0;}
    .agent-box { background-color: #262730; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #00BFFF; color: white;}
    .screen-card { background-color: #1E1E1E; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 10px; display: flex; justify-content: space-between;}
    .bull-tag { background-color: rgba(0, 208, 156, 0.2); color: #00D09C; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;}
    .bear-tag { background-color: rgba(255, 82, 82, 0.2); color: #FF5252; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;}
    hr { border-color: #333; }
</style>
""", unsafe_allow_html=True)

st.sidebar.image("https://img.icons8.com/fluency/96/000000/bullish.png", width=60)
st.sidebar.title("Aegis Dark Terminal")
page = st.sidebar.radio("Menu", ["📊 Explore & Technicals", "⚡ Top Movers & Screens", "🤖 AI Swarm Fund", "🚀 IPO & GMP Center"])
st.sidebar.markdown("---")

col1, col2 = st.sidebar.columns(2)
exchange = col1.selectbox("Market", ["NSE", "US"])
raw_ticker = col2.text_input("Asset", value="RELIANCE").upper()

ticker = f"{raw_ticker}.NS" if (exchange == "NSE" and not raw_ticker.endswith(".NS") and not raw_ticker.startswith("^")) else raw_ticker
currency = "₹" if "NSE" in exchange else "$"

if page == "📊 Explore & Technicals":
    st.title("📈 Stock Overview & Technicals")
    
    if st.sidebar.button("Analyze Stock", type="primary"):
        with st.spinner("Fetching Data..."):
            df = fetch_advanced_data(ticker, "6mo")
            
        if not df.empty:
            current_price = df['Close'].iloc[-1]
            rsi = df['RSI'].iloc[-1]
            pivots = calculate_pivot_points(df)
            
            st.markdown(f"<h2>{raw_ticker} <span style='color:gray; font-size: 20px;'>{exchange}</span></h2>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: #00BFFF;'>{currency}{current_price:.2f}</h1>", unsafe_allow_html=True)
            
            tab_overview, tab_tech = st.tabs(["Overview", "Technicals"])
            
            with tab_overview:
                fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
                fig.update_layout(height=400, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
                
            with tab_tech:
                st.markdown("### Summary (Based on 1D data)")
                g_col1, g_col2 = st.columns([1, 1])
                
                with g_col1:
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number", value = rsi, title = {'text': "Technical Sentiment (RSI)", 'font': {'size': 18, 'color': 'white'}},
                        gauge = {'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"}, 'bar': {'color': "#00BFFF"}, 'bgcolor': "#1E1E1E", 'borderwidth': 2, 'bordercolor': "#333",
                            'steps': [{'range': [0, 40], 'color': "#FF5252"}, {'range': [40, 60], 'color': "#555555"}, {'range': [60, 100], 'color': "#00D09C"}]}
                    ))
                    fig_gauge.update_layout(height=300, font={'color': "white"}, paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_gauge, use_container_width=True)
                    
                with g_col2:
                    st.markdown("### Support and Resistance")
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    st.markdown(f"**R3**: {currency}{pivots['R3']:.2f}")
                    st.markdown(f"**R2**: {currency}{pivots['R2']:.2f}")
                    st.markdown(f"**R1**: {currency}{pivots['R1']:.2f}")
                    st.markdown(f"<hr style='margin:5px;'><div style='text-align:center; background:#333; border-radius:5px; padding:3px;'><strong>PIVOT {currency}{pivots['Pivot']:.2f}</strong></div><hr style='margin:5px;'>", unsafe_allow_html=True)
                    st.markdown(f"**S1**: {currency}{pivots['S1']:.2f}")
                    st.markdown(f"**S2**: {currency}{pivots['S2']:.2f}")
                    st.markdown(f"**S3**: {currency}{pivots['S3']:.2f}")
                    st.markdown("</div>", unsafe_allow_html=True)

elif page == "⚡ Top Movers & Screens":
    st.title("⚡ Top Movers & Trading Screens")
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.markdown("### Top Movers Today")
        # Hardcoded static display mimicking Groww UI
        st.markdown("""
        <div class="metric-card">
            <table style="width:100%; text-align:left;">
                <tr style="color:gray; border-bottom:1px solid #333;">
                    <th style="padding-bottom:10px;">Company</th>
                    <th style="padding-bottom:10px;">Market Price (1D)</th>
                    <th style="padding-bottom:10px;">Volume</th>
                </tr>
                <tr>
                    <td style="padding:15px 0;"><strong>ITC</strong></td>
                    <td>₹425.50 <br><span style="color:#00D09C;">+11.00 (2.5%)</span></td>
                    <td>3,10,30,528</td>
                </tr>
                <tr>
                    <td style="padding:15px 0;"><strong>Vedanta</strong></td>
                    <td>₹264.00 <br><span style="color:#00D09C;">+10.90 (4.3%)</span></td>
                    <td>1,15,77,993</td>
                </tr>
                <tr>
                    <td style="padding:15px 0;"><strong>LTM</strong></td>
                    <td>₹4,070.00 <br><span style="color:#00D09C;">+155.00 (3.9%)</span></td>
                    <td>3,68,658</td>
                </tr>
                <tr>
                    <td style="padding:15px 0;"><strong>HDFC Bank</strong></td>
                    <td>₹1,430.00 <br><span style="color:#FF5252;">-12.50 (0.8%)</span></td>
                    <td>2,10,40,111</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Note: Values mocked for UI layout demonstration.")

    with col_side:
        st.markdown("### Trading Screens")
        
        st.markdown("""
        <div class="screen-card">
            <div>
                <span class="bull-tag">Bullish</span><br><br>
                <strong>Resistance breakouts</strong>
            </div>
            <div style="color:#00D09C; font-size:24px;">📈</div>
        </div>
        
        <div class="screen-card">
            <div>
                <span class="bull-tag">Bullish</span><br><br>
                <strong>MACD above signal line</strong>
            </div>
            <div style="color:#00D09C; font-size:24px;">📊</div>
        </div>
        
        <div class="screen-card">
            <div>
                <span class="bear-tag">Bearish</span><br><br>
                <strong>RSI overbought</strong>
            </div>
            <div style="color:#FF5252; font-size:24px;">📉</div>
        </div>
        
        <div class="screen-card">
            <div>
                <span class="bull-tag">Bullish</span><br><br>
                <strong>RSI oversold</strong>
            </div>
            <div style="color:#00D09C; font-size:24px;">📉</div>
        </div>
        """, unsafe_allow_html=True)


elif page == "🤖 AI Swarm Fund":
    st.title("🛡️ Aegis: Multi-Agent AI Swarm")
    
    if st.sidebar.button("Deploy AI Swarm", type="primary"):
        with st.spinner(f"Fetching Institutional Data for {ticker}..."):
            df = fetch_advanced_data(ticker, "2y")
            
            if df is None or df.empty or 'RSI' not in df.columns:
                st.error(f"⚠️ Insufficient historical trading data to analyze {raw_ticker}. The AI requires at least 50 days of market history to compute Technical Indicators. Please try a widely traded stock (like RELIANCE, TCS, or AAPL).")
            else:
                current_price = df['Close'].iloc[-1]
                
                with st.spinner("Training ML Model & Scraping News..."):
                    forecast_prices, ml_confidence = run_quant_forecast(df)
                    swarm_result = run_aegis_swarm(ticker, current_price, forecast_prices, ml_confidence, df)
                
                tab1, tab2 = st.tabs(["AI Verdict", "Account Growth Backtest"])
                with tab1:
                    exec_data = swarm_result['execution']
                    decision_color = "#00D09C" if exec_data['decision'] == "BUY" else "#FF5252" if exec_data['decision'] == "SELL" else "gray"
                    st.markdown(f"<h2 style='color: {decision_color};'>ACTION: {exec_data['decision']} (Confidence: {exec_data['confidence_score']}%)</h2>", unsafe_allow_html=True)
                    
                    for log in swarm_result['logs']:
                        st.markdown(f"<div class='agent-box'><strong>{log['agent']}</strong><br>{log['content']}</div>", unsafe_allow_html=True)
                
                with tab2:
                    bt_df, bt_metrics = run_backtest(df)
                    if bt_df is not None:
                        st.success("Backtest Complete: Initial Capital ₹10,000")
                        fig_bt = go.Figure()
                        fig_bt.add_trace(go.Scatter(x=bt_df['Date'], y=bt_df['Buy_Hold_Portfolio'], mode='lines', name='Buy & Hold'))
                        fig_bt.add_trace(go.Scatter(x=bt_df['Date'], y=bt_df['AI_Portfolio'], mode='lines', name='Aegis Managed', line=dict(color='#00BFFF', width=2)))
                        fig_bt.update_layout(height=400, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig_bt, use_container_width=True)

elif page == "🚀 IPO & GMP Center":
    st.title("🚀 Upcoming IPOs & Grey Market Premium (GMP)")
    st.markdown("Live tracking of upcoming IPOs, estimated listing gains, and subscription status.")
    
    st.markdown("""
    <div class="metric-card">
        <table style="width:100%; text-align:left; border-collapse: collapse;">
            <tr style="color:gray; border-bottom:1px solid #333;">
                <th style="padding-bottom:10px;">Company</th>
                <th style="padding-bottom:10px;">Opening date</th>
                <th style="padding-bottom:10px;">Est. GMP</th>
            </tr>
            <tr style="border-bottom:1px solid #333;">
                <td style="padding:15px 0;"><strong>HD Fire Protect</strong></td>
                <td>13 Oct</td>
                <td><span style="color:#00D09C;">+₹12 (15%)</span></td>
            </tr>
            <tr style="border-bottom:1px solid #333;">
                <td style="padding:15px 0;"><strong>Ravita Engineering Services (SME)</strong></td>
                <td>13 Oct</td>
                <td><span style="color:#FF5252;">-₹2 (-1%)</span></td>
            </tr>
            <tr style="border-bottom:1px solid #333;">
                <td style="padding:15px 0;"><strong>Fusion CX</strong></td>
                <td>14 Oct</td>
                <td><span style="color:#00D09C;">+₹25 (20%)</span></td>
            </tr>
            <tr style="border-bottom:1px solid #333;">
                <td style="padding:15px 0;"><strong>Zetwerk</strong></td>
                <td>To be announced</td>
                <td><span style="color:gray;">TBA</span></td>
            </tr>
            <tr style="border-bottom:1px solid #333;">
                <td style="padding:15px 0;"><strong>Reliance JIO</strong></td>
                <td>To be announced</td>
                <td><span style="color:#00D09C;">+₹85 (Expected)</span></td>
            </tr>
            <tr style="border-bottom:1px solid #333;">
                <td style="padding:15px 0;"><strong>Zepto</strong></td>
                <td>To be announced</td>
                <td><span style="color:#00D09C;">+₹45 (Expected)</span></td>
            </tr>
            <tr>
                <td style="padding:15px 0;"><strong>Razorpay</strong></td>
                <td>To be announced</td>
                <td><span style="color:gray;">TBA</span></td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Disclaimer: GMP (Grey Market Premium) is highly volatile and indicative only. Sourced from community channels.")
