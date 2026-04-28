import streamlit as st
from utils import run_query
from components.header import render_header
from components.style import apply_style

apply_style()
render_header("Sources")   # ← change per page
st.title("📥 Sources")

st.markdown("""
### 🧠 What this shows

Raw data coming from different systems:
- CRM → customers
- Core banking → accounts

👉 These systems are NOT aligned
""")

st.subheader("CRM Customers")
st.dataframe(run_query("SELECT * FROM crm_customers"))

st.subheader("Core Banking Accounts")
st.dataframe(run_query("SELECT * FROM core_banking_accounts"))