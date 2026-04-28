import streamlit as st
from utils import run_query
from components.header import render_header
from components.style import apply_style

apply_style()
render_header("Core")   # ← change per page
st.title("🧠 Core Model")

st.markdown("""
### 🧠 Core Abstraction

- PARTY → unified identity
- AGREEMENT → account/contract
- EVENT → transaction

👉 This removes duplication across systems
""")

st.subheader("Party")
st.dataframe(run_query("SELECT * FROM core_party"))

st.subheader("Agreement")
st.dataframe(run_query("SELECT * FROM core_agreement"))

st.subheader("Event")
st.dataframe(run_query("SELECT * FROM core_event"))