import os
import google.generativeai as genai

def initialize_genai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def generate_agent_debate(ticker, current_price, forecast_prices):
    """Orchestrates a debate between different AI personas based on ML data."""
    has_api = initialize_genai()
    
    trend = "upward" if forecast_prices[-1] > current_price else "downward"
    pct_change = abs(((forecast_prices[-1] - current_price) / current_price) * 100)
    
    prompt_context = f"The stock is {ticker}. The current price is ${current_price:.2f}. An ML model has forecast the price over the next 7 days to trend {trend} by {pct_change:.2f}%, ending at around ${forecast_prices[-1]:.2f}."

    if not has_api:
        # Fallback Mock Data for demo purposes if no API key is provided
        return mock_debate(ticker, trend, pct_change)
        
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Agent 1: Conservative
        cons_prompt = f"You are a conservative AI financial analyst. Read this context and argue whether to Buy, Sell, or Hold. Be cautious, focus on risks. Context: {prompt_context}. Limit to 3 sentences."
        cons_resp = model.generate_content(cons_prompt).text
        
        # Agent 2: Aggressive
        agg_prompt = f"You are an aggressive AI financial day trader. The conservative agent said: '{cons_resp}'. Rebut their argument and argue your own Buy/Sell/Hold case based on the same context: {prompt_context}. Focus on momentum and high returns. Limit to 3 sentences."
        agg_resp = model.generate_content(agg_prompt).text
        
        # Agent 3: Moderator
        mod_prompt = f"You are the Moderator AI. The conservative agent said: '{cons_resp}'. The aggressive agent said: '{agg_resp}'. Based on this debate, make a final consensus decision (Buy, Sell, or Hold) and give a 2 sentence justification."
        mod_resp = model.generate_content(mod_prompt).text
        
        return [
            {"role": "Conservative Agent (Risk-Averse)", "content": cons_resp},
            {"role": "Aggressive Agent (Momentum-Driven)", "content": agg_resp},
            {"role": "Moderator (Final Consensus)", "content": mod_resp}
        ]
    except Exception as e:
        print(f"API Error: {e}")
        return mock_debate(ticker, trend, pct_change)

def mock_debate(ticker, trend, pct_change):
    action = "BUY" if trend == "upward" else "SELL"
    return [
        {"role": "Conservative Agent (Risk-Averse)", "content": f"Given the {trend} forecast of {pct_change:.2f}%, I am cautious. We must consider market volatility before acting on {ticker}. I recommend Hold until we see stronger signals."},
        {"role": "Aggressive Agent (Momentum-Driven)", "content": f"Volatility is where the money is! The ML indicates a clear {trend} trend. We should capitalize on {ticker} immediately and take an aggressive position."},
        {"role": "Moderator (Final Consensus)", "content": f"After weighing the risks from the conservative side and the ML momentum from the aggressive side, the consensus is to {action}. {action} {ticker} with a stop-loss in place to mitigate downside."}
    ]
