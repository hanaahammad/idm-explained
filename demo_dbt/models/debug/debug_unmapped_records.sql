-- models/debug/debug_unmapped_records.sql

SELECT 
    s.customer_id

FROM {{ ref('stg_core_accounts') }} s
LEFT JOIN {{ ref('party_identifier') }} p
    ON p.source_id = s.customer_id

WHERE p.party_id IS NULL