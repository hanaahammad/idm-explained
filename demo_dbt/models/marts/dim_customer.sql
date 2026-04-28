SELECT
    party_id AS customer_key,
    name
FROM {{ ref('core_party') }}
WHERE party_type = 'PERSON'