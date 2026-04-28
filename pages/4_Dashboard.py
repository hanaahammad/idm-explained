import streamlit as st
from utils import run_query

from components.header import render_header
from components.style import apply_style

apply_style()
render_header("Dashboard")   # ← change per page

st.title("📊 Dashboard")

df = run_query("SELECT * FROM customer_360")

if df is None or df.empty:
    st.warning("No data available")
else:
    total = df["balance"].sum()
    st.metric("💰 Total Balance", f"${total:,.0f}")

    st.bar_chart(df.set_index("name")["balance"])
    st.dataframe(df)

st.markdown("""
### 🧠 What this shows

- Customer 360 aggregation
- Business metrics powered by surrogate keys
""")