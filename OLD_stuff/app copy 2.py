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


tab_theory, tab_sources, tab_core, tab_semantic, tab_business, tab_graph, tab_dashboard, tab_debug, tab_lineage, tab_explorer = st.tabs([
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
    st.header("📚 Industry Data Model (IDM)")

    st.markdown("""
## 🎯 What problem are we solving?

Traditional data models are:
- System-centric (CRM, Core Banking, etc.)
- Hard to integrate
- Duplicated identities

👉 Example:
- Same customer exists in CRM and Core Banking with different IDs

---

## 🧠 IDM Approach (FSDM-style)

We shift to **business abstraction instead of systems**:

| Concept | Meaning |
|--------|--------|
| PARTY | Any entity (Customer, Bank, Company) |
| AGREEMENT | Contract (Account, Loan, Card) |
| EVENT | Something that happens (Payment, Transaction) |

---

## 🔑 Key Idea: PARTY abstraction

👉 A PARTY can be:
- A customer 👤
- The bank 🏦
- A company 🏢

➡️ Everything becomes **a relationship between parties**

---

## 🔗 ID Mapping (Critical!)

We map different system IDs into one:

| Source | ID | → PARTY_ID |
|------|----|-----------|
| CRM | CRM123 | P001 |
| Core | CUST456 | P001 |

👉 This enables:
- Customer 360
- Clean joins
- No duplication

---

## 💡 Why this matters

Without IDM:
❌ Broken joins  
❌ Duplicate customers  
❌ Inconsistent analytics  

With IDM:
✅ Unified view  
✅ Clean joins  
✅ Business-driven analytics  

---

## 🎤 What you say in demo

> “Instead of modeling systems, we model business concepts like Party, Agreement, and Event—allowing us to unify data across systems and build a true Customer 360.”
""")
    
# =====================================================
# SOURCES
# =====================================================
with tab_sources:
    st.header("📥 Source Systems")

    st.subheader("CRM Customers")
    st.dataframe(run_query("SELECT * FROM crm_customers"))

    st.subheader("Core Banking")
    st.dataframe(run_query("SELECT * FROM core_banking_accounts"))

# =====================================================
# CORE MODEL
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

    st.subheader("DIM CUSTOMER")
    st.dataframe(run_query("SELECT * FROM dim_customer"))

    st.subheader("FACT ACCOUNT")
    st.dataframe(run_query("SELECT * FROM fact_account"))

    st.subheader("FACT EVENT")
    st.dataframe(run_query("SELECT * FROM fact_event"))

# =====================================================
# BUSINESS
# =====================================================
with tab_business:
    st.header("📊 Business Queries")

    total = run_query("SELECT SUM(balance) FROM fact_account").iloc[0,0]
    avg = run_query("SELECT AVG(balance) FROM fact_account").iloc[0,0]

    col1, col2 = st.columns(2)
    col1.metric("Total Balance", f"${total:,.0f}")
    col2.metric("Average Balance", f"${avg:,.0f}")

    st.subheader("👤 Customer 360")

    customers = run_query("SELECT DISTINCT name FROM customer_360")
    selected = st.selectbox("Select Customer", customers["name"])

    df = run_query(f"SELECT * FROM customer_360 WHERE name = '{selected}'")
    st.dataframe(df)

# =====================================================
# GRAPH (BUSINESS RELATIONSHIP)
# =====================================================


with tab_graph:
    st.header("🌐 Business Relationship Graph")

    st.success("""
💡 “This graph shows how customers, the bank, accounts, and events are connected through a unified model.”
""")

    net = Network(height="650px", width="100%")

    # Disable physics (NO DRIFT)
    net.set_options("""
    var options = {
      "physics": { "enabled": false }
    }
    """)

    # =========================
    # NODES (POSITIONED)
    # =========================

    # Parties
    net.add_node("P001", label="Alice", x=0, y=0, color="blue")
    net.add_node("P002", label="Bob", x=0, y=150, color="blue")
    net.add_node("P003", label="Charlie", x=0, y=300, color="blue")

    net.add_node("BANK", label="Bank", x=0, y=450, color="orange")

    # Accounts
    net.add_node("A123", label="Account A123", x=300, y=100, color="green")
    net.add_node("A456", label="Account A456", x=300, y=250, color="green")
    net.add_node("A789", label="Account A789", x=300, y=400, color="green")

    # Events
    net.add_node("E1", label="Payment", x=600, y=250, color="red")

    # =========================
    # EDGES
    # =========================

    # Customer → Account
    net.add_edge("P001", "A123")
    net.add_edge("P002", "A456")
    net.add_edge("P003", "A789")

    # Bank → Account
    net.add_edge("BANK", "A123")
    net.add_edge("BANK", "A456")
    net.add_edge("BANK", "A789")

    # Account → Event
    net.add_edge("A123", "E1")
    net.add_edge("A456", "E1")
    net.add_edge("A789", "E1")

    # =========================
    # RENDER
    # =========================
    net.save_graph("business_graph.html")
    st.iframe("business_graph.html", height=650)

    # =========================
    # LEGEND
    # =========================
    st.markdown("""
### 🎨 Legend
- 🔵 Customer (Party - Person)
- 🟠 Bank (Party - Organization)
- 🟢 Account (Agreement)
- 🔴 Event (Payment)

---

### 🧠 How to read it

1. Customers and the Bank are both **PARTIES**
2. They are linked to **ACCOUNTS (Agreements)**
3. Accounts generate **EVENTS (Payments)**

👉 This is the core of the Industry Data Model
""")
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

    query = st.text_area("SQL", "SELECT * FROM fact_account")

    if st.button("Run Query"):
        st.dataframe(run_query(query))

# =====================================================
# LINEAGE (INTERACTIVE + CLEAN)
# =====================================================
with tab_lineage:
    st.header("🔗 Data Lineage")

    highlight = st.checkbox("🔥 Highlight Customer 360 path", True)

    net = Network(height="600px", width="100%", directed=True)

    nodes = [
        ("CRM", "CRM", 0, 0, "gold"),
        ("CoreBank", "Core Banking", 0, 200, "gold"),
        ("stg_crm", "Staging CRM", 200, 0, "lightblue"),
        ("stg_core", "Staging Core", 200, 200, "lightblue"),
        ("party", "PARTY", 400, 0, "green"),
        ("agreement", "AGREEMENT", 400, 200, "green"),
        ("dim", "DIM CUSTOMER", 600, 0, "violet"),
        ("fact", "FACT ACCOUNT", 600, 200, "violet"),
        ("mart", "Customer 360", 800, 100, "red"),
    ]

    for id, label, x, y, color in nodes:
        net.add_node(id, label=label, x=x, y=y, color=color, physics=False)

    edges = [
        ("CRM", "stg_crm"),
        ("CoreBank", "stg_core"),
        ("stg_crm", "party"),
        ("stg_core", "agreement"),
        ("party", "dim"),
        ("agreement", "fact"),
        ("dim", "mart"),
        ("fact", "mart"),
    ]

    for e in edges:
        color = "red" if highlight and e in [("dim","mart"),("fact","mart")] else "gray"
        net.add_edge(e[0], e[1], color=color)

    net.set_options("""{ "physics": { "enabled": false } }""")

    net.save_graph("lineage.html")
    st.iframe("lineage.html", height=600)

    st.subheader("🔎 Explore Node Data")

    node_map = {
        "CRM": "SELECT * FROM crm_customers",
        "CoreBank": "SELECT * FROM core_banking_accounts",
        "stg_crm": "SELECT * FROM stg_crm_customers",
        "stg_core": "SELECT * FROM stg_core_accounts",
        "party": "SELECT * FROM core_party",
        "agreement": "SELECT * FROM core_agreement",
        "dim": "SELECT * FROM dim_customer",
        "fact": "SELECT * FROM fact_account",
        "mart": "SELECT * FROM customer_360"
    }

    selected_node = st.selectbox("Select node", list(node_map.keys()))
    st.code(node_map[selected_node])
    st.dataframe(run_query(node_map[selected_node]))


with tab_explorer:
    st.header("🔍 Interactive Explorer")

    st.success("""
💡 Explore customers, accounts, and payments dynamically.
""")

    # =====================================================
    # FILTER
    # =====================================================
    customers = {
        "All": None,
        "Alice": "P001",
        "Bob": "P002",
        "Charlie": "P003"
    }

    selected_customer = st.selectbox("Filter by Customer", list(customers.keys()))
    selected_party = customers[selected_customer]

    # =====================================================
    # DATA DISPLAY
    # =====================================================
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
        st.subheader("All Customers")
        st.dataframe(run_query("SELECT * FROM customer_360"))

    # =====================================================
    # QUICK SQL
    # =====================================================
    st.subheader("💻 SQL Console")

    query = st.text_area("Run SQL", "SELECT * FROM fact_account")

    if st.button("Run Query"):
        result = run_query(query)
        if result is not None:
            st.dataframe(result)

    # =====================================================
    # INSIGHT PANEL
    # =====================================================
    st.markdown("""
### 🧠 What this shows

- Unified customer identity (P001, etc.)
- Accounts linked via AGREEMENT
- Payments captured as EVENTS

---

### 🎤 Demo line

> “We can dynamically explore any customer and immediately access their full financial context.”
""")