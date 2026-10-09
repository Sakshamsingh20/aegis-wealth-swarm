import yfinance as yf
import pandas as pd
import numpy as np
import ta
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

def fetch_advanced_data(ticker, period="2y"):
    """Fetches stock data and calculates Advanced Technical Indicators."""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    df.reset_index(inplace=True)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    
    if len(df) < 50:
        return df # Not enough data
        
    # Feature Engineering (Technical Indicators)
    # 1. Momentum
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()
    df['MACD'] = ta.trend.MACD(close=df['Close']).macd()
    
    # 2. Volatility
    bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()
    df['ATR'] = ta.volatility.AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14).average_true_range()
    
    # 3. Trend
    df['SMA_50'] = ta.trend.SMAIndicator(close=df['Close'], window=50).sma_indicator()
    df['SMA_200'] = ta.trend.SMAIndicator(close=df['Close'], window=200).sma_indicator()
    
    # Clean NaN values caused by rolling windows
    df = df.bfill().fillna(0)
    
    return df

def run_quant_forecast(df, days_to_forecast=7):
    """Trains a Gradient Boosting model on TA features to predict forward returns."""
    if df.empty or len(df) < 50:
        return [], 0
        
    # Target: Price 7 days from now
    df['Target'] = df['Close'].shift(-days_to_forecast)
    
    # Features
    features = ['Close', 'RSI', 'MACD', 'ATR', 'SMA_50']
    
    # Training Data (drop the last N days where target is NaN)
    train_df = df.dropna(subset=['Target'])
    X = train_df[features]
    y = train_df['Target']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Model
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_scaled, y)
    
    # Predict Future
    last_row = df[features].iloc[-1:]
    last_row_scaled = scaler.transform(last_row)
    
    # Create a synthetic trajectory based on the momentum of the prediction
    final_pred = model.predict(last_row_scaled)[0]
    current_price = df['Close'].iloc[-1]
    
    # Linear interpolation for the 7 days between current and final pred (simplified trajectory)
    step = (final_pred - current_price) / days_to_forecast
    predictions = [current_price + (step * i) for i in range(1, days_to_forecast + 1)]
    
    confidence = model.score(X_scaled, y) * 100 # R^2 as proxy for model confidence
    
    return predictions, max(0, confidence)
