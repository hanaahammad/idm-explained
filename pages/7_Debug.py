import streamlit as st
from utils import run_query


from components.header import render_header
from components.style import apply_style

apply_style()
render_header("Debug")   # ← change per page


st.title("🧪 Debug")

st.markdown("""
### 🧠 What this shows

Helps diagnose:
- Join issues
- Missing mappings
- Data inconsistencies
""")

# =========================
# JOIN DEBUG
# =========================
st.subheader("🔍 Join Debug")

debug_df = run_query("SELECT * FROM debug_customer_360")

if debug_df is not None:
    total = len(debug_df)
    matches = (debug_df["join_status"] == "MATCH").sum() if "join_status" in debug_df.columns else 0
    no_match = total - matches

    c1, c2, c3 = st.columns(3)
    c1.metric("Total", total)
    c2.metric("Matches", matches)
    c3.metric("No Match", no_match)

    if no_match > 0:
        st.error("🚨 Join issues detected")
    else:
        st.success("✅ All joins are valid")

    st.dataframe(debug_df)

# =========================
# BASE TABLES (quick view)
# =========================
st.subheader("📦 Base Tables")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**dim_customer**")
    st.dataframe(run_query("SELECT * FROM dim_customer"))

with col2:
    st.markdown("**fact_account**")
    st.dataframe(run_query("SELECT * FROM fact_account"))

# =========================
# SQL CONSOLE (RESTORED)
# =========================
st.markdown("---")
st.subheader("💻 SQL Console")

query = st.text_area(
    "Enter SQL",
    value="SELECT * FROM fact_account",
    height=120,
    key="debug_sql_input"
)

if st.button("Run Query", key="debug_run_query_btn"):
    result = run_query(query)

    if result is not None:
        st.dataframe(result)
    else:
        st.warning("Query returned no results or failed")

st.markdown("""
### 🎤 Demo tip

> “We can debug data issues live by querying the warehouse directly.”
""")