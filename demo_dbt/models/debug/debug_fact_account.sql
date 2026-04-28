-- models/debug/debug_fact_account.sql

SELECT 
    customer_key,
    COUNT(*) AS record_count,
    SUM(balance) AS total_balance,

    CASE 
        WHEN customer_key IS NULL THEN '❌ NULL KEY'
        ELSE 'OK'
    END AS key_status

FROM {{ ref('fact_account') }}
GROUP BY customer_key