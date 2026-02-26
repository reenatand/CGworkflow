import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="Quant Signal Explainer", layout="wide")

st.title("📊 Fixed Income Quant Research – Signal Explainer Dashboard")
st.markdown(
"""
This dashboard demonstrates how financial news and insider reports can be 
processed into **sentiment-driven trading signals** for portfolio managers.

It simulates:
- NLP sentiment analysis on financial reports
- Signal detection
- Confidence scoring
- Actionable recommendations
"""
)

# ---- Sample stock universe (top tech names) ----
stocks = ["Apple", "Microsoft", "NVIDIA", "Amazon", "Alphabet"]

# ---- Simulated sentiment engine ----
def generate_sentiment():
    score = np.round(np.random.normal(0.1, 0.6), 2)
    return score

def signal_from_sentiment(score):
    if score > 0.35:
        return "BUY"
    elif score < -0.25:
        return "SELL"
    else:
        return "HOLD"

def confidence(score):
    return int(min(95, max(55, abs(score)*100 + random.randint(0,10))))

def justification(stock, score):
    if score > 0.35:
        return f"Positive insider commentary and strong institutional positioning suggest upside momentum in {stock}."
    elif score < -0.25:
        return f"Negative forward guidance and cautious analyst tone indicate downside risk in {stock}."
    else:
        return f"Mixed sentiment signals and neutral positioning suggest limited directional conviction in {stock}."

# ---- Build dataframe ----
rows = []
for stock in stocks:
    sent = generate_sentiment()
    rows.append({
        "Stock": stock,
        "Sentiment Score": sent,
        "Signal": signal_from_sentiment(sent),
        "Confidence (%)": confidence(sent),
        "Justification": justification(stock, sent)
    })

df = pd.DataFrame(rows)

# ---- Dashboard Layout ----
col1, col2 = st.columns([2,1])

with col1:
    st.subheader("📈 Generated Trading Signals")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("⚙️ Model Controls")
    noise = st.slider("Signal Sensitivity", 0.1, 1.0, 0.6)
    refresh = st.button("Regenerate Signals")

    if refresh:
        st.experimental_rerun()

# ---- Visualization ----
st.subheader("📊 Sentiment Distribution")
st.bar_chart(df.set_index("Stock")["Sentiment Score"])

# ---- Explainability Section ----
st.subheader("🔎 Signal Explanation")

selected = st.selectbox("Select a stock to inspect", stocks)

row = df[df["Stock"] == selected].iloc[0]

st.markdown(f"""
**Signal:** {row['Signal']}  
**Confidence:** {row['Confidence (%)']}%  
**Sentiment Score:** {row['Sentiment Score']}

**Rationale:**  
{row['Justification']}
""")

# ---- Footer ----
st.markdown("---")
st.caption(
"""
This demo simulates a production research workflow in which qualitative financial text 
is transformed into quantitative trading signals to support portfolio decision-making.
"""
)

