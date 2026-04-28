import streamlit as st

STEPS = [
    ("Sources", "pages/1_Sources.py"),
    ("Core", "pages/2_Core.py"),
    ("Semantic", "pages/3_Semantic.py"),
    ("Dashboard", "pages/4_Dashboard.py"),
    ("Lineage", "pages/5_Lineage.py"),
    ("Explorer", "pages/6_Explorer.py"),
    ("Debug", "pages/7_Debug.py"),
    ("Timeline", "pages/8_Timeline.py"),
]

def render_header(current_name: str):
    # --- Title ribbon
    st.markdown(f"### 🧭 {current_name}")

    # --- Progress
    idx = next((i for i, (n, _) in enumerate(STEPS) if n == current_name), 0)
    progress = (idx + 1) / len(STEPS)
    st.progress(progress)

    # --- Breadcrumb (clickable)
    cols = st.columns(len(STEPS))
    for i, (name, page) in enumerate(STEPS):
        label = f"**{name}**" if i == idx else name
        with cols[i]:
            st.page_link(page, label=label)

    # --- Prev / Next
    st.markdown("")
    c1, c2 = st.columns([1,1])
    with c1:
        if idx > 0:
            st.page_link(STEPS[idx-1][1], label=f"⬅️ {STEPS[idx-1][0]}")
    with c2:
        if idx < len(STEPS)-1:
            st.page_link(STEPS[idx+1][1], label=f"{STEPS[idx+1][0]} ➡️")

    st.markdown("---")