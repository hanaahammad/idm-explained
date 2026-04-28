
  
    
    

    create  table
      "demo_dbt"."main"."core_event__dbt_tmp"
  
    as (
      WITH base AS (
    SELECT
        account_no,
        ROW_NUMBER() OVER () AS rn
    FROM "demo_dbt"."main"."stg_core_accounts"
)

-- OPEN for everyone
SELECT
    'E_OPEN_' || account_no AS event_id,
    'OPEN' AS event_type,
    'A' || account_no AS agreement_id,
    CURRENT_DATE - INTERVAL 30 DAY AS event_date
FROM base

UNION ALL

-- PAYMENT for everyone
SELECT
    'E_PAY_' || account_no,
    'PAYMENT',
    'A' || account_no,
    CURRENT_DATE - INTERVAL (10 + rn) DAY
FROM base

UNION ALL

-- TRANSFER only for some customers
SELECT
    'E_TRF_' || account_no,
    'TRANSFER',
    'A' || account_no,
    CURRENT_DATE - INTERVAL (5 + rn) DAY
FROM base
WHERE rn % 2 = 1

UNION ALL

-- CLOSE only for last customer
SELECT
    'E_CLOSE_' || account_no,
    'CLOSE',
    'A' || account_no,
    CURRENT_DATE - INTERVAL 1 DAY
FROM base
WHERE rn = 3
    );
  
  