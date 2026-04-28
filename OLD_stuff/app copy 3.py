import streamlit as st
import duckdb
import networkx as nx
from pyvis.network import Network

# =====================================================
# SHARED STATE (Explorer ↔ Lineage)
# =====================================================
if "shared_selected" not in st.session_state:
    st.session_state.shared_selected = None

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
(
    tab_theory,
    tab_sources,
    tab_core,
    tab_semantic,
    tab_business,
    tab_graph,
    tab_dashboard,
    tab_debug,
    tab_lineage,
    tab_explorer
) = st.tabs([
    "📚 Theory",
    "1️⃣ Sources",
    "2️⃣ Core Model",
    "3️⃣ Semantic Layer",
    "4️⃣ Business Queries",
    "5️⃣ Data Graph",
    "6️⃣ Dashboard ⭐",
    "🧪 Debug",
    "🔗 Lineage",
    "🔍 Explorer"
])

# =====================================================
# THEORY
# =====================================================
with tab_theory:
    st.header("📚 Industry Data Model")

    st.markdown("""
### 🎯 Problem
Multiple systems → duplicate customers → broken analytics

### 🧠 Solution
Model business concepts instead:

- PARTY → who  
- AGREEMENT → contract  
- EVENT → what happens  

### 🔗 Identity Mapping
CRM + Core → unified PARTY_ID (P001)

### 🎤 Demo line
> “We model business, not systems—this enables Customer 360.”
""")

# =====================================================
# SOURCES
# =====================================================
with tab_sources:
    st.header("📥 Sources")

    st.subheader("CRM")
    st.dataframe(run_query("SELECT * FROM crm_customers"))

    st.subheader("Core Banking")
    st.dataframe(run_query("SELECT * FROM core_banking_accounts"))

# =====================================================
# CORE
# =====================================================
with tab_core:
    st.header("🧠 Core Model")

    st.dataframe(run_query("SELECT * FROM core_party"))
    st.dataframe(run_query("SELECT * FROM core_agreement"))
    st.dataframe(run_query("SELECT * FROM core_event"))

    st.subheader("🏷️ Roles")
    st.dataframe(run_query("""
        SELECT 
            a.agreement_id,
            p.name,
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
    st.dataframe(run_query("SELECT * FROM fact_event"))

# =====================================================
# BUSINESS
# =====================================================
with tab_business:
    st.header("📊 Business View")

    total = run_query("SELECT SUM(balance) FROM fact_account").iloc[0, 0]
    avg = run_query("SELECT AVG(balance) FROM fact_account").iloc[0, 0]

    col1, col2 = st.columns(2)
    col1.metric("Total Balance", f"${total:,.0f}")
    col2.metric("Avg Balance", f"${avg:,.0f}")

    st.subheader("Customer 360")

    customers = run_query("SELECT DISTINCT name FROM customer_360")
    selected = st.selectbox("Customer", customers["name"], key="business_customer")

    st.dataframe(run_query(f"""
        SELECT * FROM customer_360
        WHERE name = '{selected}'
    """))

# =====================================================
# GRAPH (SIMPLE + STABLE)
# =====================================================
with tab_graph:
    st.header("🌐 Business Relationship Graph")

    st.success("""
💡 “Customers and the bank are modeled as parties connected through accounts, and events happen on those accounts.”
""")

    net = Network(height="650px", width="100%")

    net.set_options("""
    var options = {
      "physics": { "enabled": false },
      "layout": { "improvedLayout": false }
    }
    """)

    # FIXED POSITIONS (clean alignment)
    net.add_node("P001", label="Alice", x=0, y=0, color="blue", physics=False)
    net.add_node("P002", label="Bob", x=0, y=150, color="blue", physics=False)
    net.add_node("P003", label="Charlie", x=0, y=300, color="blue", physics=False)

    net.add_node("BANK", label="Bank", x=0, y=450, color="orange", physics=False)

    net.add_node("A123", label="Account A123", x=350, y=75, color="green", physics=False)
    net.add_node("A456", label="Account A456", x=350, y=225, color="green", physics=False)
    net.add_node("A789", label="Account A789", x=350, y=375, color="green", physics=False)

    net.add_node("E1", label="Payment", x=700, y=225, color="red", physics=False)

    net.add_edges([
        ("P001","A123"), ("P002","A456"), ("P003","A789"),
        ("BANK","A123"), ("BANK","A456"), ("BANK","A789"),
        ("A123","E1"), ("A456","E1"), ("A789","E1")
    ])

    net.save_graph("business_graph.html")
    st.iframe("business_graph.html", height=650)

    st.markdown("""
### 🎨 Legend
- 🔵 Customer (Party - Person)
- 🟠 Bank (Party - Organization)
- 🟢 Account (Agreement)
- 🔴 Event (Payment)

👉 Clean left → right business flow
""")

# =====================================================
# DASHBOARD
# =====================================================
with tab_dashboard:
    st.header("📊 Dashboard")

    df = run_query("SELECT * FROM customer_360")

    if df is not None and not df.empty:
        st.bar_chart(df.set_index("name"))
        st.dataframe(df)

# =====================================================
# DEBUG
# =====================================================
with tab_debug:
    st.header("🧪 Debug")

    df = run_query("SELECT * FROM debug_customer_360")

    if df is not None:
        st.metric("Matches", len(df[df["join_status"] == "✅ MATCH"]))
        st.dataframe(df)

    st.subheader("SQL Console")

    query = st.text_area("Query", "SELECT * FROM fact_account", key="debug_sql")

    if st.button("Run Query", key="debug_run"):
    
        st.dataframe(run_query(query))

# =====================================================
# LINEAGE
# =====================================================
with tab_lineage:
    st.header("🔗 Data Lineage (Interactive)")

    st.success("""
💡 Click a table in Explorer → it highlights here  
💡 Select a node → opens it in Explorer
""")

    highlight = st.checkbox("🔥 Highlight Customer 360 path", True, key="lineage_highlight")

    selected = st.session_state.shared_selected

    net = Network(height="600px", width="100%", directed=True)

    net.set_options("""
    var options = {
      "physics": { "enabled": false },
      "layout": { "improvedLayout": false }
    }
    """)

    nodes = [
        ("crm_customers", "CRM", 0, 0, "gold"),
        ("core_banking_accounts", "Core Banking", 0, 200, "gold"),

        ("stg_crm_customers", "Staging CRM", 250, 0, "lightblue"),
        ("stg_core_accounts", "Staging Core", 250, 200, "lightblue"),

        ("core_party", "PARTY", 500, 0, "green"),
        ("core_agreement", "AGREEMENT", 500, 200, "green"),

        ("dim_customer", "DIM CUSTOMER", 750, 0, "violet"),
        ("fact_account", "FACT ACCOUNT", 750, 200, "violet"),

        ("customer_360", "Customer 360", 1000, 100, "red"),
    ]

    # ADD NODES (with highlight)
    for id, label, x, y, color in nodes:

        node_color = color
        size = 20

        if selected == id:
            node_color = "yellow"   # 🔥 highlight
            size = 35

        net.add_node(id, label=label, x=x, y=y, color=node_color, size=size, physics=False)

    edges = [
        ("crm_customers","stg_crm_customers"),
        ("core_banking_accounts","stg_core_accounts"),
        ("stg_crm_customers","core_party"),
        ("stg_core_accounts","core_agreement"),
        ("core_party","dim_customer"),
        ("core_agreement","fact_account"),
        ("dim_customer","customer_360"),
        ("fact_account","customer_360")
    ]

    for e in edges:
        color = "red" if highlight and e in [("dim_customer","customer_360"),("fact_account","customer_360")] else "gray"
        net.add_edge(e[0], e[1], color=color)

    net.save_graph("lineage_interactive.html")
    st.iframe("lineage_interactive.html", height=600)

    # =====================================================
    # NODE SELECTOR (Lineage → Explorer)
    # =====================================================
    st.subheader("🔎 Select Node")

    node_options = [n[0] for n in nodes]

    chosen = st.selectbox("Select a node", node_options, key="lineage_select")

    if st.button("Open in Explorer", key="lineage_open"):
        st.session_state.shared_selected = chosen
        st.session_state.selected_table = chosen
        st.success(f"Opened {chosen} in Explorer")

    st.markdown("""
### 🧠 Layers Explained

- 🟡 Sources → CRM, Core Banking  
- 🔵 Staging → raw ingestion  
- 🟢 Core → business abstraction (PARTY, AGREEMENT)  
- 🟣 Semantic → DIM / FACT  
- 🔴 Analytics → Customer 360  

👉 This is the full data pipeline
""")
    

# =====================================================
# EXPLORER (FIXED + WORKING CLICK + HORIZONTAL)
# =====================================================
with tab_explorer:
    st.header("🔍 Interactive Explorer")

    st.success("""
💡 Explore the warehouse and click any table to inspect its data.
""")
# Sync with lineage
if st.session_state.shared_selected:
    st.session_state.selected_table = st.session_state.shared_selected
    # =====================================================
    # SESSION STATE (DO NOT RESET ON RERUN)
    # =====================================================
    if "selected_table" not in st.session_state:
        st.session_state.selected_table = None

    # =====================================================
    # 🏗️ WAREHOUSE EXPLORER (HORIZONTAL - CLICKABLE)
    # =====================================================
    st.subheader("🏗️ Warehouse Explorer")
    st.caption("Flow: Staging → Core → Semantic → Analytics")

    tables_df = run_query("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'main'
    """)

    if tables_df is not None:

        all_tables = tables_df["table_name"].tolist()

        layers = {
            "🔵 Staging": [t for t in all_tables if t.startswith("stg_")],
            "🟢 Core": [t for t in all_tables if t.startswith("core_") or t in ["party_identifier", "agreement_party_role"]],
            "🟣 Semantic": [t for t in all_tables if t.startswith("dim_") or t.startswith("fact_")],
            "🔴 Analytics": [t for t in all_tables if "customer_360" in t]
        }

        cols = st.columns(len(layers))

        for i, (layer, tables) in enumerate(layers.items()):
            with cols[i]:
                st.markdown(f"### {layer}")

                with st.container(border=True):
                    for t in tables:
                        if st.button(t, key=f"explore_btn_{t}"):
                            st.session_state.selected_table = t
                            st.session_state.shared_selected = t   # 🔥 send to lineage
                            

    # =====================================================
    # 📊 DISPLAY SELECTED TABLE (PERSISTENT)
    # =====================================================
    if st.session_state.selected_table:
        st.markdown(f"## 📊 Table: `{st.session_state.selected_table}`")

        df = run_query(f"SELECT * FROM {st.session_state.selected_table}")

        if df is not None:
            st.dataframe(df)
            st.caption(f"Rows: {len(df)}")

    # =====================================================
    # 👤 CUSTOMER EXPLORATION (UNCHANGED LOGIC)
    # =====================================================
    st.markdown("---")
    st.subheader("👤 Customer Exploration")

    customers = {
        "All": None,
        "Alice": "P001",
        "Bob": "P002",
        "Charlie": "P003"
    }

    selected_customer = st.selectbox(
        "Filter by Customer",
        list(customers.keys()),
        key="explorer_customer_filter"
    )

    selected_party = customers[selected_customer]

    if selected_party:
        st.subheader("Customer Details")
        st.dataframe(run_query(f"""
            SELECT * FROM dim_customer 
            WHERE customer_key = '{selected_party}'
        """))

        st.subheader("Accounts")
        st.dataframe(run_query(f"""
            SELECT * FROM fact_account 
            WHERE customer_key = '{selected_party}'
        """))

        st.subheader("Customer 360")
        st.dataframe(run_query(f"""
            SELECT * FROM customer_360 
            WHERE customer_key = '{selected_party}'
        """))
    else:
        st.dataframe(run_query("SELECT * FROM customer_360"))

    # =====================================================
    # 💻 SQL CONSOLE (NO DUPLICATE BUG)
    # =====================================================
    st.markdown("---")
    st.subheader("💻 SQL Console")

    query = st.text_area(
        "Run SQL",
        "SELECT * FROM fact_account",
        key="explorer_sql_input"
    )

    if st.button("Run Query", key="explorer_sql_run"):
        result = run_query(query)
        if result is not None:
            st.dataframe(result)

    # =====================================================
    # 🧠 EXPLANATION (DEMO VALUE)
    # =====================================================
    st.markdown("""
### 🧠 What this shows

- The warehouse is organized by **layers (Staging → Core → Semantic → Analytics)**
- Each layer has a specific role in data transformation
- You can explore any dataset instantly
- You can drill down to a specific customer view

---

### 🎤 Demo line

> “We can navigate the warehouse like a data catalog, from raw ingestion to business-ready datasets, and explore any table or customer instantly.”
""")
   