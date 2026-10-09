# 🛡️ Aegis: Autonomous Wealth Swarm

**The ultimate fusion of Quantitative Finance, Generative AI, and Agentic Swarms.**

Aegis is an institutional-grade portfolio simulator that transcends basic AI chatbots. It simulates a fully autonomous hedge fund by combining advanced Machine Learning, real-time news scraping, and a multi-agent AI debate system to make data-driven financial decisions.

## 🌟 Next-Level Architecture
1. **Quantitative ML Engine (`quant_engine.py`):** Uses the `ta` library to compute RSI, MACD, and Bollinger Bands. Trains a `GradientBoostingRegressor` to predict 7-day forward returns based on technical momentum.
2. **Account Growth Simulator (`backtester.py`):** A custom backtesting engine that simulates what would happen if you gave the AI Swarm $10,000 two years ago. Compares the AI's equity curve against traditional Buy & Hold.
3. **News Sentiment Scraper:** Uses `BeautifulSoup` to scrape live Yahoo Finance headlines to inject real-world macroeconomic context into the AI.
4. **Agentic Swarm (`swarm_agents.py`):** Utilizes Google Gemini to spawn highly specialized agents (Macro-Economist, Quant Analyst, Risk Manager). They debate the ML data and output a structured JSON consensus for the Execution Engine.

## 🚀 How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Dashboard:**
   ```bash
   streamlit run app.py
   ```

## 🌐 How to Deploy (For Free)
To show this off to 10M+ people on LinkedIn, deploy it to Streamlit Community Cloud:
1. Push this repository to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Click "New App", select your GitHub repository, and type `app.py` as the Main file path.
4. Click Deploy! In 2 minutes, you will have a public URL to share on your resume and LinkedIn.
