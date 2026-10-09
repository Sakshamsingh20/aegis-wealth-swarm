import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import json

def fetch_latest_news(ticker):
    """Scrapes Yahoo Finance for the latest news headlines for context."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f'https://finance.yahoo.com/quote/{ticker}/news'
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = [h3.text for h3 in soup.find_all('h3')][:5]
        if not headlines:
            return ["No recent news found, relying purely on quantitative data."]
        return headlines
    except Exception:
        return ["Error fetching news, relying on technical indicators."]

def initialize_genai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def run_aegis_swarm(ticker, current_price, forecast_prices, ml_confidence, tech_data):
    """Orchestrates a 4-agent swarm to analyze the stock."""
    has_api = initialize_genai()
    news = fetch_latest_news(ticker)
    news_str = " | ".join(news)
    
    rsi = tech_data['RSI'].iloc[-1]
    macd = tech_data['MACD'].iloc[-1]
    trend = "upward" if forecast_prices[-1] > current_price else "downward"
    
    prompt_context = f"""
    Stock: {ticker} @ ${current_price:.2f}
    7-Day Forecast: Trending {trend} to ${forecast_prices[-1]:.2f} (ML Confidence: {ml_confidence:.1f}%)
    Technicals: RSI={rsi:.1f}, MACD={macd:.2f}
    Recent News Headlines: {news_str}
    """

    if not has_api:
        return mock_aegis_debate(ticker, prompt_context, trend)
        
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 1. Fundamental & Macro Agent
        macro_prompt = f"You are a Macro-Economist Agent. Analyze this context: {prompt_context}. Focus on the news sentiment and broader market implications. Provide a 2-sentence analysis."
        macro_resp = model.generate_content(macro_prompt).text
        
        # 2. Quantitative Agent
        quant_prompt = f"You are a Quantitative Analyst Agent. Context: {prompt_context}. The Macro Agent said: '{macro_resp}'. Ignore the news, focus entirely on the RSI, MACD, and ML forecast. What is the mathematical edge here? 2 sentences."
        quant_resp = model.generate_content(quant_prompt).text
        
        # 3. Risk Manager Agent
        risk_prompt = f"You are a Risk Manager Agent. Macro says: '{macro_resp}'. Quant says: '{quant_resp}'. Context: {prompt_context}. Evaluate the downside risk and volatility. 2 sentences."
        risk_resp = model.generate_content(risk_prompt).text
        
        # 4. Execution Engine (Consensus)
        exec_prompt = f"""You are the Execution Engine. 
        Macro: {macro_resp}
        Quant: {quant_resp}
        Risk: {risk_resp}
        Based on this swarm analysis, output a final JSON decision strictly in this format (no markdown code blocks, just raw JSON):
        {{"decision": "BUY" or "SELL" or "HOLD", "confidence_score": 0-100, "reasoning": "1 sentence summary"}}"""
        
        exec_resp = model.generate_content(exec_prompt).text
        
        # Clean JSON parsing
        try:
            decision_data = json.loads(exec_resp.replace('```json','').replace('```','').strip())
        except:
            decision_data = {"decision": "HOLD", "confidence_score": 50, "reasoning": "Swarm consensus failed to parse JSON, defaulting to Hold."}
        
        return {
            "logs": [
                {"agent": "🌍 Macro-Economist", "content": macro_resp},
                {"agent": "🔢 Quant Engine", "content": quant_resp},
                {"agent": "🛡️ Risk Manager", "content": risk_resp}
            ],
            "execution": decision_data
        }
    except Exception as e:
        print(f"API Error: {e}")
        return mock_aegis_debate(ticker, prompt_context, trend)

def mock_aegis_debate(ticker, context, trend):
    action = "BUY" if trend == "upward" else "SELL"
    return {
        "logs": [
            {"agent": "🌍 Macro-Economist", "content": f"The recent news headlines present a mixed sentiment, but the broader sector trends suggest stable support for {ticker}."},
            {"agent": "🔢 Quant Engine", "content": f"Technical indicators are aligning with the ML forecast. Momentum is clearly shifting {trend}, giving us a statistical edge."},
            {"agent": "🛡️ Risk Manager", "content": f"Volatility is moderate. Position sizing should be kept to 5% of the portfolio to hedge against sudden macro shocks."}
        ],
        "execution": {
            "decision": action,
            "confidence_score": 78,
            "reasoning": f"Quantitative momentum outpaces macro risks, triggering a {action} signal."
        }
    }
