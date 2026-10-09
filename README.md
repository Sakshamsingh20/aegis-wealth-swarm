# 🤖 FinSwarm: Agentic Portfolio Simulator

An intermediate-level AI/ML project showcasing the powerful combination of Machine Learning (Time-Series Forecasting), Generative AI, and Agentic workflows.

## 🌟 Overview
FinSwarm is an interactive web dashboard built with Streamlit. It demonstrates a complex AI pipeline:
1. **Machine Learning:** Pulls real-time financial data using `yfinance` and runs a linear regression time-series forecast to predict future stock movements.
2. **Generative AI:** Uses LLMs (Google Gemini) to synthesize the numerical data into natural language.
3. **Agentic AI:** Spawns multiple AI agents with distinct personas (Conservative Risk-Averse vs. Aggressive Momentum-Driven). The agents ingest the ML forecast and debate one another before a Moderator agent steps in to issue a final Buy/Hold/Sell consensus.

This project perfectly illustrates how AI can move beyond just Chatbots into autonomous, decision-making workflows based on statistical data.

## 🚀 Features
*   **Live Data:** Fetches real market history using `yfinance`.
*   **ML Forecasting:** Uses scikit-learn to predict 7-day future price movements.
*   **Agentic Debate:** Connects to the Gemini API to trigger dynamic prompt-chained debates between AI personas.
*   **Interactive UI:** Beautiful data visualization using Plotly within a Streamlit app.
*   **API Fallback:** Automatically falls back to a mock engine if no API key is provided, ensuring the demo always works for recruiters!

## 🛠️ Installation & Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repo-url>
   cd finswarm_project
   ```

2. **Install Dependencies:**
   Make sure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Set API Key:**
   To enable the real AI Agent debate, set your Gemini API key:
   *   **Windows:** `set GEMINI_API_KEY="your-api-key"`
   *   **Mac/Linux:** `export GEMINI_API_KEY="your-api-key"`

4. **Run the App:**
   ```bash
   streamlit run app.py
   ```

## 🧠 Why this project stands out on a resume:
Instead of just calling an API, this project demonstrates **AI Engineering**. It shows you can build full-stack data apps, handle data manipulation (`pandas`, `numpy`), apply statistical modeling (`scikit-learn`), and engineer complex LLM workflows (Agentic Debates) in a cohesive, user-friendly product.

---
*Built as a portfolio piece to demonstrate applied Agentic AI & ML.*
