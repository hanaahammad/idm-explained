import streamlit as st
import time

st.set_page_config(layout="wide")

# -----------------------------------
# 🎨 Styling (cinematic)
# -----------------------------------
st.markdown("""
<style>
.centered {
    text-align: center;
    margin-top: 100px;
}
.title {
    font-size: 40px;
    font-weight: bold;
}
.subtitle {
    font-size: 20px;
    color: gray;
}
.fade {
    animation: fadeIn 1s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# 🎬 Title screen
# -----------------------------------
st.markdown("""
<div class="centered fade">
    <div class="title">🏦 Industry Data Model Demo</div>
    <div class="subtitle">From Raw Data → Customer Insight</div>
</div>
""", unsafe_allow_html=True)

time.sleep(2)

st.markdown("---")

# -----------------------------------
# 🎞️ Steps (cinematic sequence)
# -----------------------------------
steps = [
    ("🔴 Problem", "Data is fragmented across systems with inconsistent identifiers"),
    ("🟡 Core Model", "We standardize identifiers and introduce surrogate keys"),
    ("🟢 Trust Layer", "We validate joins and ensure data consistency"),
    ("🔵 Business View", "We build a Customer 360 aggregated view"),
    ("🟣 Insight", "We visualize customer behavior over time"),
]

for title, desc in steps:
    st.markdown(f"""
    <div class="centered fade">
        <div class="title">{title}</div>
        <div class="subtitle">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2.5)
    st.markdown("---")

# -----------------------------------
# 🎯 Final message
# -----------------------------------
st.markdown("""
<div class="centered fade">
    <div class="title">🎯 Outcome</div>
    <div class="subtitle">
        Clean • Trusted • Actionable Data
    </div>
</div>
""", unsafe_allow_html=True)

time.sleep(2)

# -----------------------------------
# 🚀 Call to action
# -----------------------------------
st.markdown("---")

st.success("👉 Now explore each step using the navigation menu")

st.page_link("pages/1_Sources.py", label="➡️ Start with Sources")