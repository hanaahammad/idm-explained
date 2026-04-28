-- models/debug/debug_join.sql

SELECT 
    d.customer_key,
    d.name,
    f.customer_key AS fact_key,
    f.balance
FROM {{ ref('dim_customer') }} d
LEFT JOIN {{ ref('fact_account') }} f
ON d.customer_key = f.customer_key