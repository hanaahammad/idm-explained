select
    a.agreement_sk,

    -- 🔥 CANONICAL CUSTOMER KEY
    'P' || LPAD(
        REGEXP_EXTRACT(CAST(acc.customer_id AS VARCHAR), '[0-9]+'),
        3,
        '0'
    ) as customer_key,

    acc.balance

from {{ ref('stg_core_accounts') }} acc
join {{ ref('core_agreement') }} a
    on acc.account_no = a.source_agreement_id