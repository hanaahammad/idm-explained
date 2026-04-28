import streamlit as st
import time

st.set_page_config(layout="wide")

# -----------------------------------
# 🎨 Styling (clean + modern)
# -----------------------------------
st.markdown("""
<style>
.block {
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid #eee;
}
.step-title {
    font-size: 22px;
    font-weight: bold;
}
.step-desc {
    font-size: 15px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# 🎬 Title
# -----------------------------------
st.title("🎬 Guided Data Journey")
st.markdown("### From raw data → trusted insight")

# -----------------------------------
# ▶️ Start demo button
# -----------------------------------
if "started" not in st.session_state:
    st.session_state.started = False

if st.button("▶️ Start Demo"):
    st.session_state.started = True

# -----------------------------------
# 🧭 Steps
# -----------------------------------
steps = [
    ("1️⃣ Sources", "Raw data from multiple systems with inconsistent identifiers"),
    ("2️⃣ Core Model", "Normalize IDs and introduce surrogate keys for consistency"),
    ("3️⃣ Semantic Layer", "Add business meaning and clean abstractions"),
    ("4️⃣ Dashboard", "Aggregate into Customer 360 view"),
    ("5️⃣ Lineage", "Trace how data flows across the pipeline"),
    ("6️⃣ Explorer", "Allow users to explore the warehouse interactively"),
    ("7️⃣ Debug", "Validate joins and detect inconsistencies"),
    ("8️⃣ Timeline", "Visualize customer behavior over time"),
]

# -----------------------------------
# 🎞️ Animated reveal
# -----------------------------------
if st.session_state.started:

    for i, (title, desc) in enumerate(steps):
        with st.container():
            st.markdown(f"""
            <div class="block">
                <div class="step-title">{title}</div>
                <div class="step-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        time.sleep(0.4)

    st.success("🎯 Outcome: Clean, trusted, and actionable customer data")

# -----------------------------------
# 🧠 Static view (before clicking)
# -----------------------------------
else:
    st.info("Click ▶️ Start Demo to walk through the journey")

# -----------------------------------
# 🚀 Navigation hints
# -----------------------------------
st.markdown("---")
st.markdown("### 🚀 How to navigate")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("👉 Start with **Sources**")

with col2:
    st.markdown("👉 Validate in **Debug**")

with col3:
    st.markdown("👉 End with **Timeline**")

# -----------------------------------
# 🎤 Speaker notes (collapsible)
# -----------------------------------
with st.expander("🎤 Speaker Notes (for demo)"):
    st.markdown("""
- Start by explaining the problem: fragmented data  
- Emphasize surrogate keys in Core  
- Show Debug to build trust  
- Highlight Dashboard for business value  
- Finish with Timeline for insight  
""")