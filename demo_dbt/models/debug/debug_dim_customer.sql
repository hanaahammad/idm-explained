-- models/debug/debug_dim_customer.sql

SELECT 
    customer_key,
    name,

    CASE 
        WHEN customer_key IS NULL THEN '❌ NULL KEY'
        ELSE 'OK'
    END AS key_status

FROM {{ ref('dim_customer') }}