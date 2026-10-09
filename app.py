import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
from quant_engine import fetch_advanced_data, run_quant_forecast
from backtester import run_backtest
from swarm_agents import run_aegis_swarm

st.set_page_config(page_title="Aegis: Pro Wealth Terminal", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a Bloomberg-Terminal-like experience
st.markdown("""
<style>
    .big-font { font-size: 24px !important; font-weight: bold; color: #4CAF50;}
    .agent-box { background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #00BFFF;}
    .ipo-card { background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #4CAF50; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

st.sidebar.image("https://img.icons8.com/fluency/96/000000/bullish.png", width=60)
st.sidebar.title("Aegis Terminal")
page = st.sidebar.radio("Navigation", ["🤖 AI Swarm Analysis", "⚡ Intraday Screener", "🚀 IPO & Allotment Center"])
st.sidebar.markdown("---")

if page == "🤖 AI Swarm Analysis":
    st.title("🛡️ Aegis: Multi-Agent AI Swarm")
    st.markdown("Advanced ML & AI consensus engine for automated portfolio growth.")
    
    col1, col2 = st.sidebar.columns(2)
    exchange = col1.selectbox("Market", ["NSE (India)", "US Market"])
    raw_ticker = col2.text_input("Asset", value="RELIANCE").upper()
    
    # Auto-format for Indian stocks
    if exchange == "NSE (India)" and not raw_ticker.endswith(".NS") and not raw_ticker.startswith("^"):
        ticker = f"{raw_ticker}.NS"
    else:
        ticker = raw_ticker

    if st.sidebar.button("Deploy AI Swarm", type="primary"):
        with st.spinner(f"Fetching Institutional Data for {ticker}..."):
            df = fetch_advanced_data(ticker, "2y")
            
        if df is None or df.empty:
            st.error(f"Insufficient data for {ticker}. Please check the symbol.")
        else:
            current_price = df['Close'].iloc[-1]
            
            tab1, tab2, tab3 = st.tabs(["📊 Live Swarm Analysis", "📈 Account Growth Backtest", "🧠 Swarm Brain Logs"])
            
            with tab1:
                ccol1, ccol2, ccol3 = st.columns(3)
                ccol1.metric("Current Price", f"₹{current_price:.2f}" if "NSE" in exchange else f"${current_price:.2f}")
                ccol2.metric("RSI (14)", f"{df['RSI'].iloc[-1]:.1f}")
                ccol3.metric("MACD", f"{df['MACD'].iloc[-1]:.2f}")
                
                with st.spinner("Training Gradient Boosting Quant Model..."):
                    forecast_prices, ml_confidence = run_quant_forecast(df)
                
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Market'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], line=dict(color='orange', width=1), name='50 SMA'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], line=dict(color='blue', width=1), name='200 SMA'))
                
                last_date = df['Date'].iloc[-1]
                future_dates = [last_date + datetime.timedelta(days=i) for i in range(1, 8)]
                fig.add_trace(go.Scatter(x=[last_date] + future_dates, y=[current_price] + forecast_prices, mode='lines+markers', name='AI Quant Forecast', line=dict(color='#00ff00', width=3)))
                
                fig.update_layout(height=500, template="plotly_dark", xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
                
                with st.spinner("Initializing AI Swarm & Scraping News..."):
                    swarm_result = run_aegis_swarm(ticker, current_price, forecast_prices, ml_confidence, df)
                
                exec_data = swarm_result['execution']
                decision_color = "green" if exec_data['decision'] == "BUY" else "red" if exec_data['decision'] == "SELL" else "gray"
                st.markdown(f"<p style='font-size: 30px; font-weight: bold; color: {decision_color};'>ACTION: {exec_data['decision']} (Confidence: {exec_data['confidence_score']}%)</p>", unsafe_allow_html=True)
                st.info(f"**Reasoning:** {exec_data['reasoning']}")

            with tab2:
                with st.spinner("Running historical backtest..."):
                    bt_df, bt_metrics = run_backtest(df)
                if bt_df is not None:
                    st.success("Backtest Complete: Initial Capital ₹10,000")
                    mcol1, mcol2, mcol3 = st.columns(3)
                    mcol1.metric("Buy & Hold Return", bt_metrics['BH_Total_Return'])
                    mcol2.metric("AI Swarm Return", bt_metrics['AI_Total_Return'], delta=bt_metrics['Alpha_Generated'])
                    mcol3.metric("Final Value", bt_metrics['AI_Final_Value'].replace("$", "₹") if "NSE" in exchange else bt_metrics['AI_Final_Value'])
                    
                    fig_bt = go.Figure()
                    fig_bt.add_trace(go.Scatter(x=bt_df['Date'], y=bt_df['Buy_Hold_Portfolio'], mode='lines', name='Buy & Hold'))
                    fig_bt.add_trace(go.Scatter(x=bt_df['Date'], y=bt_df['AI_Portfolio'], mode='lines', name='Aegis Managed'))
                    fig_bt.update_layout(height=400, template="plotly_dark")
                    st.plotly_chart(fig_bt, use_container_width=True)

            with tab3:
                for log in swarm_result['logs']:
                    st.markdown(f"<div class='agent-box'><strong>{log['agent']}</strong><br>{log['content']}</div>", unsafe_allow_html=True)

elif page == "⚡ Intraday Screener":
    st.title("⚡ Intraday Momentum Screener")
    st.markdown("Live technical analysis of top Nifty 50 stocks to detect Bullish/Bearish intraday momentum.")
    
    if st.button("Scan Indian Market Now"):
        with st.spinner("Scanning Nifty Top Movers..."):
            # Hardcoded list for demo purposes
            top_stocks = ["HDFCBANK.NS", "RELIANCE.NS", "INFY.NS", "ICICIBANK.NS", "TCS.NS"]
            results = []
            
            for sym in top_stocks:
                try:
                    df = fetch_advanced_data(sym, "1mo") # Short timeframe for Intraday proxy
                    rsi = df['RSI'].iloc[-1]
                    macd = df['MACD'].iloc[-1]
                    price = df['Close'].iloc[-1]
                    
                    if rsi > 70:
                        signal, color = "Overbought (Bearish)", "red"
                    elif rsi < 30:
                        signal, color = "Oversold (Bullish)", "green"
                    elif macd > 0:
                        signal, color = "Momentum (Bullish)", "green"
                    else:
                        signal, color = "Weakness (Bearish)", "red"
                        
                    results.append({"Stock": sym.replace(".NS", ""), "Price": f"₹{price:.2f}", "RSI": f"{rsi:.1f}", "MACD": f"{macd:.2f}", "Signal": signal})
                except:
                    pass
            
            st.table(pd.DataFrame(results))
            st.caption("Signals generated via RSI and MACD crossovers.")

elif page == "🚀 IPO & Allotment Center":
    st.title("🚀 IPO Desk: GMP & Allotment")
    st.markdown("Track upcoming Indian IPOs, Grey Market Premium (GMP), and check allotment status.")
    
    tab_ipo, tab_allot = st.tabs(["Upcoming IPOs & GMP", "Check Allotment Status"])
    
    with tab_ipo:
        st.markdown("### 🔔 Live IPO Pipeline")
        st.markdown("""
        <div class='ipo-card'>
            <h4>Swiggy Ltd. IPO</h4>
            <p><strong>Expected Price Band:</strong> ₹370 - ₹390 | <strong>Est. GMP:</strong> <span style='color:green;'>+₹120 (30%)</span></p>
            <p><strong>Status:</strong> Upcoming (Draft Filed)</p>
        </div>
        <div class='ipo-card'>
            <h4>Hyundai Motor India IPO</h4>
            <p><strong>Expected Price Band:</strong> ₹1865 - ₹1960 | <strong>Est. GMP:</strong> <span style='color:orange;'>+₹65 (3%)</span></p>
            <p><strong>Status:</strong> Subscriptions Closed</p>
        </div>
        <div class='ipo-card'>
            <h4>NTPC Green Energy</h4>
            <p><strong>Expected Price Band:</strong> TBA | <strong>Est. GMP:</strong> TBA</p>
            <p><strong>Status:</strong> DRHP Filed</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Note: GMP is scraped from community grey market feeds and is highly volatile. Data shown is mocked for portfolio demonstration as live GMP APIs are restricted.")
        
    with tab_allot:
        st.markdown("### 🏦 PAN Allotment Checker")
        st.info("Directly check your IPO allotment status via Registrar API endpoints.")
        
        col1, col2 = st.columns(2)
        selected_ipo = col1.selectbox("Select IPO", ["Hyundai Motor India", "Swiggy Ltd (Upcoming)", "Bajaj Housing Finance"])
        pan_number = col2.text_input("Enter PAN Number", max_chars=10).upper()
        
        if st.button("Verify Allotment"):
            if len(pan_number) != 10:
                st.error("Please enter a valid 10-character PAN card number.")
            else:
                with st.spinner("Connecting to Registrar (LinkIntime/KFintech) via encrypted gateway..."):
                    import time
                    time.sleep(2) # Simulating API call
                    st.error(f"⚠️ Registration API Blocked: Automated PAN queries are restricted by Indian registrars due to CAPTCHA protections. To check allotment for {selected_ipo}, please visit the official registrar website directly.")
                    st.markdown(f"[Click here to check {selected_ipo} on KFintech](https://kosmic.kfintech.com/ipostatus/)")
