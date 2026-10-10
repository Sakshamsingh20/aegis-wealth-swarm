import yfinance as yf
import pandas as pd
import numpy as np
import ta
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

def fetch_advanced_data(ticker, period="2y"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    df.reset_index(inplace=True)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    
    if len(df) < 50:
        return df 
        
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()
    df['MACD'] = ta.trend.MACD(close=df['Close']).macd()
    
    bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()
    df['ATR'] = ta.volatility.AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14).average_true_range()
    
    df['SMA_50'] = ta.trend.SMAIndicator(close=df['Close'], window=50).sma_indicator()
    df['SMA_200'] = ta.trend.SMAIndicator(close=df['Close'], window=200).sma_indicator()
    
    df = df.bfill().fillna(0)
    return df

def calculate_pivot_points(df):
    """Calculates standard Support & Resistance levels like Groww."""
    if len(df) < 2: return {}
    last_day = df.iloc[-2] # Use yesterday's data for today's pivots
    
    h = last_day['High']
    l = last_day['Low']
    c = last_day['Close']
    
    p = (h + l + c) / 3
    return {
        "R3": h + 2 * (p - l),
        "R2": p + (h - l),
        "R1": (p * 2) - l,
        "Pivot": p,
        "S1": (p * 2) - h,
        "S2": p - (h - l),
        "S3": l - 2 * (h - p)
    }

def run_quant_forecast(df, days_to_forecast=7):
    if df.empty or len(df) < 50: return [], 0
    df['Target'] = df['Close'].shift(-days_to_forecast)
    features = ['Close', 'RSI', 'MACD', 'ATR', 'SMA_50']
    
    train_df = df.dropna(subset=['Target'])
    X = train_df[features]
    y = train_df['Target']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_scaled, y)
    
    last_row = df[features].iloc[-1:]
    last_row_scaled = scaler.transform(last_row)
    
    final_pred = model.predict(last_row_scaled)[0]
    current_price = df['Close'].iloc[-1]
    
    step = (final_pred - current_price) / days_to_forecast
    predictions = [current_price + (step * i) for i in range(1, days_to_forecast + 1)]
    confidence = model.score(X_scaled, y) * 100 
    
    return predictions, max(0, confidence)
