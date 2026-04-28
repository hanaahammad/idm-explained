import streamlit as st

def apply_style():
    st.markdown("""
    <style>
    .stApp { background-color: #fafafa; }
    div[data-testid="stMetric"] {
        border-radius: 10px;
        padding: 10px;
        background: white;
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)