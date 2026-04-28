import streamlit as st
from utils import run_query

from components.header import render_header
from components.style import apply_style

apply_style()
render_header("Semantic")   # ← change per page

st.title("⭐ Semantic Layer")

st.markdown("""
### 🧠 Business Layer

- DIM → descriptive
- FACT → measurable

👉 Ready for analytics
""")

st.subheader("Customers")
st.dataframe(run_query("SELECT * FROM dim_customer"))

st.subheader("Accounts")
st.dataframe(run_query("SELECT * FROM fact_account"))

st.subheader("Events")
st.dataframe(run_query("SELECT * FROM fact_event"))