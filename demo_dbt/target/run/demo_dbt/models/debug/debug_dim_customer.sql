
  
  create view "demo_dbt"."main"."debug_dim_customer__dbt_tmp" as (
    -- models/debug/debug_dim_customer.sql

SELECT 
    customer_key,
    name,

    CASE 
        WHEN customer_key IS NULL THEN '❌ NULL KEY'
        ELSE 'OK'
    END AS key_status

FROM "demo_dbt"."main"."dim_customer"
  );
