SELECT
    'A' || account_no AS agreement_id,
    p.party_id,
    'OWNER' AS role_type
FROM {{ ref('stg_core_accounts') }} s
JOIN {{ ref('party_identifier') }} p
    ON p.source_id = s.customer_id
    AND p.source_system = 'CORE'

UNION ALL

SELECT
    'A' || account_no,
    'P_BANK',
    'ISSUER'
FROM {{ ref('stg_core_accounts') }}