-- models/debug/debug_summary.sql

SELECT
    COUNT(*) AS total_records,

    SUM(CASE WHEN p.party_id IS NULL THEN 1 ELSE 0 END) AS unmapped_records,

    ROUND(
        100.0 * SUM(CASE WHEN p.party_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS mapping_success_rate

FROM {{ ref('stg_core_accounts') }} s
LEFT JOIN {{ ref('party_identifier') }} p
    ON p.source_id = s.customer_id