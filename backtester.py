import pandas as pd
import numpy as np

def run_backtest(df, initial_capital=10000.0):
    """
    Simulates AI account growth vs Buy & Hold over the dataset.
    AI Strategy: If SMA_50 > SMA_200 (Golden Cross) and RSI < 70, hold stock. Else, hold cash.
    This is a simplified proxy for the AI's daily decision logic.
    """
    if len(df) < 200:
        return None, None
        
    backtest_df = df.copy()
    
    # Buy & Hold Logic
    initial_price = backtest_df['Close'].iloc[0]
    backtest_df['Buy_Hold_Shares'] = initial_capital / initial_price
    backtest_df['Buy_Hold_Portfolio'] = backtest_df['Buy_Hold_Shares'] * backtest_df['Close']
    
    # AI Swarm Logic (Moving Average + Momentum crossover system)
    cash = initial_capital
    shares = 0
    portfolio_value = []
    
    for i in range(len(backtest_df)):
        row = backtest_df.iloc[i]
        price = row['Close']
        sma50 = row['SMA_50']
        sma200 = row['SMA_200']
        rsi = row['RSI']
        
        # AI Decision
        bullish = sma50 > sma200 and rsi < 75
        bearish = sma50 < sma200 or rsi > 80
        
        if bullish and cash > 0:
            # Buy
            shares = cash / price
            cash = 0
        elif bearish and shares > 0:
            # Sell
            cash = shares * price
            shares = 0
            
        current_val = cash + (shares * price)
        portfolio_value.append(current_val)
        
    backtest_df['AI_Portfolio'] = portfolio_value
    
    # Metrics
    ai_return = ((backtest_df['AI_Portfolio'].iloc[-1] - initial_capital) / initial_capital) * 100
    bh_return = ((backtest_df['Buy_Hold_Portfolio'].iloc[-1] - initial_capital) / initial_capital) * 100
    
    metrics = {
        'AI_Total_Return': f"{ai_return:.2f}%",
        'BH_Total_Return': f"{bh_return:.2f}%",
        'AI_Final_Value': f"${backtest_df['AI_Portfolio'].iloc[-1]:,.2f}",
        'Alpha_Generated': f"{(ai_return - bh_return):.2f}%"
    }
    
    return backtest_df, metrics
