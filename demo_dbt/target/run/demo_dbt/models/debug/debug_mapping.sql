
  
  create view "demo_dbt"."main"."debug_mapping__dbt_tmp" as (
    -- models/debug/debug_mapping.sql

SELECT 
    s.customer_id,
    p.party_id,

    CASE 
        WHEN p.party_id IS NULL THEN '❌ NOT MAPPED'
        ELSE '✅ MAPPED'
    END AS mapping_status

FROM "demo_dbt"."main"."stg_core_accounts" s
LEFT JOIN "demo_dbt"."main"."party_identifier" p
    ON p.source_id = s.customer_id
  );
