import streamlit as st
from pyvis.network import Network
from components.header import render_header
from components.style import apply_style

apply_style()
render_header("Lineage")   # ← change per page


st.title("🔗 Data Lineage")

st.markdown("""
### 🧠 What this shows

How data flows across layers:
Source → Core → Semantic → Analytics
""")

net = Network(height="600px", width="100%", directed=True)
net.set_options("""{ "physics": { "enabled": false } }""")

nodes = [
    "crm_customers",
    "core_party",
    "dim_customer",
    "fact_account",
    "customer_360"
]

for n in nodes:
    net.add_node(n)

net.add_edges([
    ("crm_customers","core_party"),
    ("core_party","dim_customer"),
    ("dim_customer","customer_360"),
    ("fact_account","customer_360")
])

net.save_graph("lineage.html")
st.components.v1.html(open("lineage.html").read(), height=600)
st.markdown("""
### 🧠 What this shows

Data flows using surrogate keys:
- agreement_sk links facts
- ensures consistency across domains
""")