import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def fetch_stock_data(ticker, period="6mo"):
    """Fetches historical stock data."""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    df.reset_index(inplace=True)
    # Remove timezone to avoid plotly issues
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    return df

def forecast_stock(df, days_to_forecast=7):
    """Predicts future prices using a simple Linear Regression model."""
    if df.empty:
        return []
    
    # Create a simple time index
    df['DayIndex'] = np.arange(len(df))
    X = df[['DayIndex']]
    y = df['Close']
    
    # Train ML Model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict future days
    last_day = df['DayIndex'].iloc[-1]
    future_X = pd.DataFrame({'DayIndex': np.arange(last_day + 1, last_day + 1 + days_to_forecast)})
    predictions = model.predict(future_X)
    
    return predictions.tolist()
