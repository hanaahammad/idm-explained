import streamlit as st
import pandas as pd
from utils import run_query


from components.header import render_header
from components.style import apply_style

apply_style()
render_header("Timeline")   # ← change per page


st.set_page_config(layout="wide")

st.title("📅 Event Timeline")

# -----------------------------------
# 🧠 What this shows
# -----------------------------------
st.markdown("""
### 🧠 What this shows
Customer activity over time using surrogate keys
""")

# -----------------------------------
# 🔽 Customer selector
# -----------------------------------
customers_df = run_query("SELECT customer_key FROM dim_customer")
customers = customers_df["customer_key"].tolist()

selected_customer = st.selectbox("Select Customer", customers)

# -----------------------------------
# 📊 Load events
# -----------------------------------
df = run_query(f"""
SELECT 
    e.event_type, 
    e.event_date,
    a.agreement_sk
FROM fact_event e
JOIN fact_account a 
    ON e.agreement_sk = a.agreement_sk
WHERE a.customer_key = '{selected_customer}'
ORDER BY e.event_date
""")

# -----------------------------------
# 🧾 Timeline display
# -----------------------------------
if df.empty:
    st.warning("No events found")
else:
    df["event_date"] = pd.to_datetime(df["event_date"])

    st.markdown("## 📍 Customer Journey")

    cols = st.columns(len(df))

    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i]:

            icon = {
                "OPEN": "🟢",
                "PAYMENT": "🔵",
                "TRANSFER": "🟣",
                "CLOSE": "🔴"
            }.get(row["event_type"], "⚪")

            st.markdown(f"""
            <div style="text-align:center">
                <div style="font-size:30px">{icon}</div>
                <div><b>{row['event_type']}</b></div>
                <div style="font-size:12px">{row['event_date'].date()}</div>
                <div style="font-size:12px;color:gray">Account: {row['agreement_sk']}</div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------
# 📈 Activity Trend
# -----------------------------------
if not df.empty:
    st.markdown("## 📈 Activity Trend")

    df["count"] = 1
    trend = df.groupby("event_date").count().cumsum()

    st.line_chart(trend["count"])