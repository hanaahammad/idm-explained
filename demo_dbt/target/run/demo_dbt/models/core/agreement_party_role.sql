
  
    
    

    create  table
      "demo_dbt"."main"."agreement_party_role__dbt_tmp"
  
    as (
      SELECT
    'A' || account_no AS agreement_id,
    p.party_id,
    'OWNER' AS role_type
FROM "demo_dbt"."main"."stg_core_accounts" s
JOIN "demo_dbt"."main"."party_identifier" p
    ON p.source_id = s.customer_id
    AND p.source_system = 'CORE'

UNION ALL

SELECT
    'A' || account_no,
    'P_BANK',
    'ISSUER'
FROM "demo_dbt"."main"."stg_core_accounts"
    );
  
  