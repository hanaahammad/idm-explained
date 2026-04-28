
  
  create view "demo_dbt"."main"."debug_join__dbt_tmp" as (
    -- models/debug/debug_join.sql

SELECT 
    d.customer_key,
    d.name,
    f.customer_key AS fact_key,
    f.balance
FROM "demo_dbt"."main"."dim_customer" d
LEFT JOIN "demo_dbt"."main"."fact_account" f
ON d.customer_key = f.customer_key
  );
