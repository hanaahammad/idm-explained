-- models/debug/debug_mapping.sql

SELECT 
    s.customer_id,
    p.party_id,

    CASE 
        WHEN p.party_id IS NULL THEN '❌ NOT MAPPED'
        ELSE '✅ MAPPED'
    END AS mapping_status

FROM {{ ref('stg_core_accounts') }} s
LEFT JOIN {{ ref('party_identifier') }} p
    ON p.source_id = s.customer_id