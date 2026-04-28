import streamlit as st

st.set_page_config(layout="wide")

# -----------------------------------
# 🏠 TITLE
# -----------------------------------
st.title("🏛️ Industry Data Model — From Systems to Analytics")

# -----------------------------------
# 🧠 FROM CHAOS TO ANALYTICS
# -----------------------------------
st.markdown("## 🧠 From Systems to Insight")

st.markdown("""
Modern enterprises operate multiple systems:

- CRM → customers  
- Billing → accounts  
- Transactions → events  

Each system describes the business differently.

### ❌ Without a core model
- duplicated logic  
- inconsistent metrics  
- fragile dashboards  

### ✅ With a core model
- unified business definitions  
- reusable transformations  
- scalable analytics  
""")

# -----------------------------------
# 🧩 SUBJECT AREAS
# -----------------------------------
st.markdown("## 🧩 Subject Areas: The Business Vocabulary")

st.markdown("""
A core data model organizes the business into **subject areas**.

Each subject area represents a fundamental concept:
""")

st.markdown("""
- **Party** → who (customers, organizations)  
- **Agreement** → contracts, accounts  
- **Product** → what is offered  
- **Event** → what happens  
- **Finance** → value & transactions  
- **Channel** → how interaction happens  
- **Location** → where it happens  
- **Organization** → internal structure  
""")

st.markdown("""
👉 Together, they form a **connected graph of the business**, not isolated tables.
""")

# -----------------------------------
# 🔗 RELATIONSHIPS
# -----------------------------------
st.markdown("## 🔗 Relationships: How Everything Connects")

st.markdown("""
Subject areas are **not independent**.

Examples:

- A **Party** owns an **Agreement**  
- An **Agreement** generates **Events**  
- An **Event** impacts **Finance**  

👉 This creates a **network of relationships** that enables analytics.
""")

# -----------------------------------
# ⚙️ WHY CORE MODEL FOR ANALYTICS
# -----------------------------------
st.markdown("## ⚙️ Why the Core Model Matters for Analytics")

st.markdown("""
The core model acts as a **semantic foundation**.

Instead of building analytics directly from raw data, we build them from standardized entities:

- Party → Customer dimension  
- Agreement → Account structure  
- Event → Fact table  
- Product → Product dimension  

### 🎯 Benefits

✔ Consistent KPIs  
✔ Reusable logic  
✔ Faster development  
✔ Easier debugging  
""")

# -----------------------------------
# 🧬 DATA GRAMMAR
# -----------------------------------
st.markdown("## 🧬 Data Grammar: How We Detect Facts & Dimensions")

st.markdown("""
We can interpret the model using a simple grammar:
""")

st.markdown("### 🧍 Nouns → Dimensions")
st.markdown("""
- Customer (Party)  
- Product  
- Location  

👉 Stable, descriptive entities
""")

st.markdown("### ⚡ Verbs → Facts")
st.markdown("""
- Payment  
- Transfer  
- Event  

👉 Something that happens over time
""")

st.markdown("### 🔗 Relationships → Keys")
st.markdown("""
- customer_key  
- agreement_sk  

👉 Connect facts to dimensions
""")

st.info("💡 Core idea: The data model behaves like a language — nouns, verbs, and relationships.")

# -----------------------------------
# 🔗 MAPPING TO YOUR DEMO
# -----------------------------------
st.markdown("## 🔗 Mapping to Our Implementation")

st.markdown("""
In this demo:

- **dim_customer** ← Party (Dimension)  
- **fact_account** ← Agreement (Structured fact / snapshot)  
- **fact_event** ← Event (Fact table)  

### 🔑 Why surrogate keys matter

They allow us to:
- unify multiple source systems  
- ensure consistent joins  
- enable reliable analytics  
""")

# -----------------------------------
# 🤖 AUTOMATION VISION
# -----------------------------------
st.markdown("## 🤖 Toward Automated Analytics Modeling")

st.markdown("""
Because the core model follows a consistent structure, we can:

👉 Automatically detect:
- Dimensions (entities with attributes)
- Facts (entities with time + measures)
- Relationships (keys)

👉 Which enables:
- automatic data marts  
- semantic layers  
- AI-assisted modeling  
""")

# -----------------------------------
# 🧪 INTERACTIVE GRAMMAR DETECTION
# -----------------------------------
st.markdown("## 🧪 Interactive Grammar Detection")

st.markdown("""
Try to classify a data entity based on its role in the model.

👉 Is it a **Dimension**, a **Fact**, or a **Relationship**?
""")

# INPUT (TEXT + DROPDOWN)
col1, col2 = st.columns([2, 1])

with col1:
    entity_input = st.text_input("Enter an entity (e.g. Customer, Payment, Account)")

with col2:
    example = st.selectbox(
        "Or pick",
        ["", "Customer", "Payment", "Agreement", "customer_key", "Transaction"]
    )

# PRIORITY LOGIC
entity = entity_input if entity_input else example

# -----------------------------------
# RULE ENGINE
# -----------------------------------
def classify_entity(name):
    name = name.lower()

    dimension_keywords = ["customer", "party", "product", "location", "organization"]
    fact_keywords = ["payment", "event", "transaction", "transfer", "activity"]
    relationship_keywords = ["id", "key", "sk", "reference"]

    if any(k in name for k in dimension_keywords):
        return "dimension", "🧍 This looks like a stable business entity (noun)."
    
    if any(k in name for k in fact_keywords):
        return "fact", "⚡ This represents something happening over time (verb)."
    
    if any(k in name for k in relationship_keywords):
        return "relationship", "🔗 This connects entities together (key/identifier)."
    
    return "unknown", "🤔 Not sure — try thinking: is it a noun, verb, or link?"

# -----------------------------------
# OUTPUT
# -----------------------------------
if entity:
    label, explanation = classify_entity(entity)

    if label == "dimension":
        st.success(f"Detected as DIMENSION\n\n{explanation}")
    elif label == "fact":
        st.warning(f"Detected as FACT\n\n{explanation}")
    elif label == "relationship":
        st.info(f"Detected as RELATIONSHIP\n\n{explanation}")
    else:
        st.write(explanation)

# -----------------------------------
# 🎤 FINAL MESSAGE
# -----------------------------------
st.markdown("## 🎤 Key Takeaway")

st.success("""
The core model is not just a data structure —  
it is a **grammar that allows us to systematically build analytics**.
""")