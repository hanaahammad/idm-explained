import streamlit as st
import pandas as pd
import time
from utils import run_query


from components.header import render_header
from components.style import apply_style

apply_style()
render_header("Timeline")   # ← change per page

import streamlit as st
import pandas as pd
from utils import run_query

st.set_page_config(layout="wide")

st.title("📅 Event Timeline")

# -----------------------------------
# 🎨 STYLE SYSTEM
# -----------------------------------
st.markdown("""
<style>
.timeline-container {
    position: relative;
    height: 30px;
    margin: 30px 0 50px 0;
}

.timeline-line {
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 4px;
    background: #e6e6e6;
    transform: translateY(-50%);
    border-radius: 2px;
}

.timeline-progress {
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #1677ff, #69b1ff);
    transform: translateY(-50%);
    border-radius: 2px;
    animation: growLine 1.2s ease forwards;
}

.timeline-dot {
    position: absolute;
    top: 50%;
    width: 14px;
    height: 14px;
    background: white;
    border: 3px solid #1677ff;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: pulse 2s infinite;
}

@keyframes growLine {
    from { width: 0%; }
    to { width: 100%; }
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(22,119,255,0.5); }
    70% { box-shadow: 0 0 0 10px rgba(22,119,255,0); }
    100% { box-shadow: 0 0 0 0 rgba(22,119,255,0); }
}

.card {
    text-align: center;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #eaeaea;
    background: white;
    transition: all 0.25s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
}

.card.selected {
    border: 3px solid #1677ff;
    background: #f5faff;
    box-shadow: 0 10px 26px rgba(22,119,255,0.15);
}
</style>
""", unsafe_allow_html=True)

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
    e.agreement_sk
FROM fact_event e
JOIN fact_account a 
    ON e.agreement_sk = a.agreement_sk
WHERE a.customer_key = '{selected_customer}'
ORDER BY e.event_date
""")

if df.empty:
    st.warning("No events found")
    st.stop()

df["event_date"] = pd.to_datetime(df["event_date"])

# -----------------------------------
# 🧭 HEADER
# -----------------------------------
st.markdown("## 📍 Customer Journey")
st.caption("🟢 Open   🔵 Payment   🟣 Transfer   🔴 Close")

# -----------------------------------
# 🔵 BUILD DOTS SAFELY (FIXED)
# -----------------------------------
dots_html = ""

for i in range(len(df)):
    if len(df) > 1:
        left = (i / (len(df) - 1)) * 100
    else:
        left = 50
    dots_html += f'<div class="timeline-dot" style="left:{left}%;"></div>'

# -----------------------------------
# 🔵 RENDER TIMELINE
# -----------------------------------
st.markdown(f"""
<div class="timeline-container">
    <div class="timeline-line"></div>
    <div class="timeline-progress"></div>
    {dots_html}
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# 🎯 EVENT CARDS
# -----------------------------------
selected_event = st.session_state.get("selected_event", None)

cols = st.columns(len(df))

for i, (_, row) in enumerate(df.iterrows()):

    is_selected = (
        selected_event is not None
        and selected_event["agreement_sk"] == row["agreement_sk"]
        and selected_event["event_type"] == row["event_type"]
    )

    icon = {
        "OPEN": "🟢",
        "PAYMENT": "🔵",
        "TRANSFER": "🟣",
        "CLOSE": "🔴"
    }.get(row["event_type"], "⚪")

    with cols[i]:

        # click handler
        if st.button("", key=f"event_{i}"):
            st.session_state["selected_event"] = row.to_dict()
            st.rerun()

        # card
        st.markdown(f"""
        <div class="card {'selected' if is_selected else ''}">
            <div style="font-size:{'36px' if is_selected else '28px'}">{icon}</div>
            <div style="font-weight:600;margin-top:6px">{row['event_type']}</div>
            <div style="font-size:13px;color:gray">{row['event_date'].date()}</div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------
# 🔍 DETAILS PANEL
# -----------------------------------
if "selected_event" in st.session_state:

    event = st.session_state["selected_event"]

    st.markdown("---")
    st.markdown("## 🔍 Event Details")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Event", event["event_type"])

    with c2:
        st.metric("Date", str(pd.to_datetime(event["event_date"]).date()))

    with c3:
        st.metric("Agreement", event["agreement_sk"])

    # account
    account_df = run_query(f"""
        SELECT agreement_sk, customer_key, balance
        FROM fact_account
        WHERE agreement_sk = {event['agreement_sk']}
    """)

    if not account_df.empty:
        st.markdown("### 💰 Account Snapshot")
        st.dataframe(account_df, use_container_width=True)

    # raw event
    with st.expander("🧾 Raw Event Data"):
        raw_event = run_query(f"""
            SELECT *
            FROM fact_event
            WHERE agreement_sk = {event['agreement_sk']}
        """)
        st.dataframe(raw_event, use_container_width=True)

# -----------------------------------
# 📈 TREND
# -----------------------------------
st.markdown("## 📈 Activity Trend")

df["count"] = 1
trend = df.groupby("event_date").count().cumsum()

st.line_chart(trend["count"])