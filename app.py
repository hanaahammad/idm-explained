import streamlit as st
import pandas as pd
from utils import run_query

st.set_page_config(layout="wide")

st.title("📅 Event Timeline")

# -----------------------------------
# Customer selector
# -----------------------------------
customers_df = run_query("SELECT customer_key FROM dim_customer")
customers = customers_df["customer_key"].tolist()

selected_customer = st.selectbox("Select Customer", customers)

# -----------------------------------
# Load events
# -----------------------------------
df = run_query(f"""
SELECT 
    e.event_type, 
    e.event_date,
    e.agreement_sk
FROM fact_event e
JOIN fact_account a 
    ON e.agreement_sk = a.agreement_sk
WHERE a.customer_key = '{selected_customer}'
ORDER BY e.event_date
""")

if df.empty:
    st.warning("No events found")
else:
    df["event_date"] = pd.to_datetime(df["event_date"])

    st.markdown("## 📍 Customer Journey")
    st.markdown("🟢 OPEN • 🔵 PAYMENT • 🟣 TRANSFER • 🔴 CLOSE")

    cols = st.columns(len(df))

    # -----------------------------------
    # Render clickable events
    # -----------------------------------
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i]:

            icon = {
                "OPEN": "🟢",
                "PAYMENT": "🔵",
                "TRANSFER": "🟣",
                "CLOSE": "🔴"
            }.get(row["event_type"], "⚪")

            if st.button(
                f"{icon}\n{row['event_type']}\n{row['event_date'].date()}",
                key=f"event_{i}"
            ):
                st.session_state["selected_event"] = row.to_dict()

# -----------------------------------
# 📊 Event Details Panel
# -----------------------------------
if "selected_event" in st.session_state:

    event = st.session_state["selected_event"]

    st.markdown("---")
    st.markdown("## 🔍 Event Details")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Event Type", event["event_type"])
        st.metric("Date", str(event["event_date"].date()))

    with col2:
        st.metric("Agreement", event["agreement_sk"])

    # -----------------------------------
    # Load related account
    # -----------------------------------
    account_df = run_query(f"""
        SELECT *
        FROM fact_account
        WHERE agreement_sk = {event['agreement_sk']}
    """)

    if not account_df.empty:
        st.markdown("### 💰 Account Details")
        st.dataframe(account_df)

    # -----------------------------------
    # Raw event
    # -----------------------------------
    raw_event = run_query(f"""
        SELECT *
        FROM fact_event
        WHERE agreement_sk = {event['agreement_sk']}
    """)

    st.markdown("### 🧾 Raw Event Data")
    st.dataframe(raw_event)