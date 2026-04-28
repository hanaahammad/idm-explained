-- models/debug/customer_360.sql

SELECT 
    d.customer_key,
    d.name,
    f.balance
FROM "demo_dbt"."main"."dim_customer" d
LEFT JOIN "demo_dbt"."main"."fact_account" f
ON d.customer_key = f.customer_key