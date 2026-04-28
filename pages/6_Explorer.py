import streamlit as st
from utils import run_query


from components.header import render_header
from components.style import apply_style

apply_style()
render_header("Explorer")   # ← change per page



st.title("🔍 Explorer")

st.markdown("""
### 🧠 What this shows

Explore any table and drill into Customer 360 using surrogate keys
""")

# =========================
# TABLE EXPLORER
# =========================
tables = run_query("SELECT table_name FROM information_schema.tables")

if tables is not None:
    selected = st.selectbox("Select table", tables["table_name"].tolist())
    st.dataframe(run_query(f"SELECT * FROM {selected}"))

# =========================
# CUSTOMER 360 (FIXED)
# =========================
st.markdown("---")
st.subheader("👤 Customer 360")

customers = run_query("SELECT DISTINCT customer_key FROM fact_account")

if customers is not None and not customers.empty:

    selected_customer = st.selectbox(
        "Select Customer",
        customers["customer_key"]
    )

    # ACCOUNTS
    account_df = run_query(f"""
        SELECT *
        FROM fact_account
        WHERE customer_key = '{selected_customer}'
    """)

    # EVENTS (FIXED WITH agreement_sk)
    event_df = run_query(f"""
        SELECT e.*
        FROM fact_event e
        JOIN fact_account a
        ON e.agreement_sk = a.agreement_sk
        WHERE a.customer_key = '{selected_customer}'
    """)

    # KPIs
    if account_df is not None and not account_df.empty:
        total = account_df["balance"].sum()
        st.metric("💰 Total Balance", f"${total:,.0f}")

        st.bar_chart(account_df.set_index("agreement_sk")["balance"])

    st.markdown("### 🏦 Accounts")
    st.dataframe(account_df)

    st.markdown("### 💳 Events")
    st.dataframe(event_df)

# =========================
# SQL
# =========================
st.markdown("---")
query = st.text_area("Run SQL", "SELECT * FROM fact_account")

if st.button("Run Query"):
    st.dataframe(run_query(query))