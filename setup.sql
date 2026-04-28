py -m venv venv
venv\Scripts\activate
pip install streamlit pandas networkx pyvis dbt-core dbt-duckdb
pip freeze > requirements.txt

project/
│
├── venv/
├── app.py
├── requirements.txt
│
├── demo_dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── staging/
│   │   ├── core/
│   │   ├── marts/
│   ├── seeds/


dbt init demo_dbt

👉 This:

Creates a new dbt project
Sets up folders (models/, seeds/, etc.)
Asks you to configure a database (choose duckdb)
🧩 Then what comes next (your exact flow)

After dbt init, do this in order:

1️⃣ Go into the project
cd demo_dbt
2️⃣ Load your seed data
dbt seed

👉 This creates tables from your CSV files
(e.g. core_banking_accounts, crm_customers)

3️⃣ Run transformations
dbt run

👉 This builds:

staging
core (PARTY / AGREEMENT / EVENT…)
marts (DIM / FACT)
4️⃣ (Optional but recommended) test
dbt test


========================================

Fix: create profiles.yml
📍 Location (VERY important)

Create this file:

C:\Users\<YOUR_USERNAME>\.dbt\profiles.yml

👉 Example:

C:\Users\Hanaa\.dbt\profiles.yml


dbt run
Check:
dbt ls
