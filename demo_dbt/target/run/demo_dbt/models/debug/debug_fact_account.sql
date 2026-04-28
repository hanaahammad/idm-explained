
  
  create view "demo_dbt"."main"."debug_fact_account__dbt_tmp" as (
    -- models/debug/debug_fact_account.sql

SELECT 
    customer_key,
    COUNT(*) AS record_count,
    SUM(balance) AS total_balance,

    CASE 
        WHEN customer_key IS NULL THEN '❌ NULL KEY'
        ELSE 'OK'
    END AS key_status

FROM "demo_dbt"."main"."fact_account"
GROUP BY customer_key
  );
