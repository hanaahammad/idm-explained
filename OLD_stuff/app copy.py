import streamlit as st
import duckdb
import networkx as nx
from pyvis.network import Network

st.set_page_config(layout="wide")

st.title("🏦 Industry Data Model Demo (FSDM-style)")

DB_PATH = "demo_dbt/demo_dbt.duckdb"

# =====================================================
# DB HELPER
# =====================================================
def run_query(query):
    try:
        with duckdb.connect(DB_PATH, read_only=True) as conn:
            return conn.execute(query).df()
    except Exception as e:
        st.error(f"SQL Error: {e}")
        return None

# =====================================================
# TABS
# =====================================================
tab_theory, tab_sources, tab_core, tab_semantic, tab_business, tab_graph, tab_dashboard, tab_debug, tab_lineage = st.tabs([
    "📚 Theory",
    "1️⃣ Sources",
    "2️⃣ Core Model",
    "3️⃣ Semantic Layer",
    "4️⃣ Business Queries",
    "5️⃣ Data Graph",
    "6️⃣ Dashboard ⭐",
    "🧪 Debug",
    "🔗 Lineage"
])

# =====================================================
# THEORY
# =====================================================
with tab_theory:
    st.header("📚 Industry Data Model")

    st.markdown("""
### 🧠 Core Concepts

- PARTY → Person or Organization  
- AGREEMENT → Account  
- EVENT → Payment  

👉 One unified structure across all systems
""")

# =====================================================
# SOURCES
# =====================================================
with tab_sources:
    st.header("📥 Sources")

    st.dataframe(run_query("SELECT * FROM core_banking_accounts"))
    st.dataframe(run_query("SELECT * FROM crm_customers"))

# =====================================================
# CORE MODEL + ROLE MODELING
# =====================================================
with tab_core:
    st.header("🧠 Core Model")

    st.subheader("PARTY")
    st.dataframe(run_query("SELECT * FROM core_party"))

    st.subheader("AGREEMENT")
    st.dataframe(run_query("SELECT * FROM core_agreement"))

    st.subheader("EVENT")
    st.dataframe(run_query("SELECT * FROM core_event"))

    st.subheader("🏷️ Roles (Bank vs Customer)")
    st.dataframe(run_query("""
        SELECT 
            a.agreement_id,
            p.name,
            p.party_type,
            r.role_type
        FROM agreement_party_role r
        JOIN core_party p ON p.party_id = r.party_id
        JOIN core_agreement a ON a.agreement_id = r.agreement_id
    """))

# =====================================================
# SEMANTIC
# =====================================================
with tab_semantic:
    st.header("⭐ Semantic Layer")

    st.dataframe(run_query("SELECT * FROM dim_customer"))
    st.dataframe(run_query("SELECT * FROM fact_account"))

# =====================================================
# BUSINESS (LOOKER STYLE)
# =====================================================
with tab_business:
    st.header("📊 Business Queries")

    # Metrics
    st.subheader("📐 Metrics")

    total_balance = run_query("SELECT SUM(balance) FROM fact_account").iloc[0,0]
    avg_balance = run_query("SELECT AVG(balance) FROM fact_account").iloc[0,0]

    col1, col2 = st.columns(2)
    col1.metric("Total Balance", f"${total_balance:,.0f}")
    col2.metric("Average Balance", f"${avg_balance:,.0f}")

    # Filter (semantic behavior)
    st.subheader("🔎 Customer 360")

    customers = run_query("SELECT DISTINCT name FROM customer_360")
    selected = st.selectbox("Select Customer", customers["name"])

    df = run_query(f"""
        SELECT * FROM customer_360
        WHERE name = '{selected}'
    """)

    st.dataframe(df)

# =====================================================
# GRAPH (BUSINESS VIEW)
# =====================================================
with tab_graph:
    st.header("🌐 Business Relationship")

    st.success("""
💡 “Customers and the Bank are both parties connected through accounts and events.”
""")

    G = nx.Graph()

    party_df = run_query("SELECT * FROM core_party")
    role_df = run_query("SELECT * FROM agreement_party_role")
    agreement_df = run_query("SELECT * FROM core_agreement")

    for _, row in party_df.iterrows():
        color = "blue" if row["party_type"] == "PERSON" else "orange"
        G.add_node(row["party_id"], label=row["name"], color=color)

    for _, row in agreement_df.iterrows():
        G.add_node(row["agreement_id"], label=row["agreement_id"], color="green")

    for _, row in role_df.iterrows():
        G.add_edge(row["party_id"], row["agreement_id"])

    net = Network(height="600px", width="100%")
    net.from_nx(G)

    net.set_options("""
    var options = {
      "physics": { "enabled": false }
    }
    """)

    net.save_graph("graph.html")
    st.iframe("graph.html", height=600)

# =====================================================
# DASHBOARD
# =====================================================
with tab_dashboard:
    st.header("📊 Dashboard")

    df = run_query("SELECT * FROM customer_360")

    if df is not None and not df.empty:
        col1, col2 = st.columns(2)
        col1.metric("Customers", df["name"].nunique())
        col2.metric("Total Balance", f"${df['balance'].sum():,.0f}")

        st.bar_chart(df.set_index("name"))
        st.dataframe(df)
    else:
        st.warning("No data — check Debug tab")

# =====================================================
# DEBUG
# =====================================================
with tab_debug:
    st.header("🧪 Debug Layer")

    join_df = run_query("SELECT * FROM debug_customer_360")

    if join_df is not None:
        total = len(join_df)
        matched = len(join_df[join_df["join_status"] == "✅ MATCH"])
        unmatched = len(join_df[join_df["join_status"] == "❌ NO MATCH"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total", total)
        col2.metric("Matches", matched)
        col3.metric("No Match", unmatched)

        st.dataframe(join_df)

    st.subheader("💻 SQL Console")

    query = st.text_area("Enter SQL:", "SELECT * FROM fact_account")

    if st.button("Run Query"):
        result = run_query(query)
        if result is not None:
            st.dataframe(result)

# =====================================================
# LINEAGE (FIXED — BOXED + CLEAN)
# =====================================================
with tab_lineage:
    st.header("🔗 Data Flow (Clean View)")

    st.success("""
💡 “Data flows from Sources → Staging → Core → Semantic → Analytics”
""")

    net = Network(height="600px", width="100%", directed=True)

    # FIXED POSITIONS (no floating!)
    net.add_node("CRM", label="CRM", x=0, y=0, color="gold", physics=False)
    net.add_node("CoreBank", label="Core Banking", x=0, y=200, color="gold", physics=False)

    net.add_node("stg_crm", label="Staging CRM", x=200, y=0, color="lightblue", physics=False)
    net.add_node("stg_core", label="Staging Core", x=200, y=200, color="lightblue", physics=False)

    net.add_node("party", label="PARTY", x=400, y=0, color="green", physics=False)
    net.add_node("agreement", label="AGREEMENT", x=400, y=200, color="green", physics=False)

    net.add_node("dim", label="DIM CUSTOMER", x=600, y=0, color="violet", physics=False)
    net.add_node("fact", label="FACT ACCOUNT", x=600, y=200, color="violet", physics=False)

    net.add_node("mart", label="Customer 360", x=800, y=100, color="red", physics=False)

    # EDGES
    net.add_edge("CRM", "stg_crm")
    net.add_edge("CoreBank", "stg_core")

    net.add_edge("stg_crm", "party")
    net.add_edge("stg_core", "agreement")

    net.add_edge("party", "dim")
    net.add_edge("agreement", "fact")

    net.add_edge("dim", "mart")
    net.add_edge("fact", "mart")

    net.set_options("""
    var options = {
      "physics": { "enabled": false }
    }
    """)

    net.save_graph("lineage_clean.html")
    st.iframe("lineage_clean.html", height=600)

    st.markdown("""
### 🎨 Legend
- 🟡 Sources  
- 🔵 Staging  
- 🟢 Core  
- 🟣 Semantic  
- 🔴 Analytics  
""")