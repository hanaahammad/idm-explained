
  
  create view "demo_dbt"."main"."debug_unmapped_records__dbt_tmp" as (
    -- models/debug/debug_unmapped_records.sql

SELECT 
    s.customer_id

FROM "demo_dbt"."main"."stg_core_accounts" s
LEFT JOIN "demo_dbt"."main"."party_identifier" p
    ON p.source_id = s.customer_id

WHERE p.party_id IS NULL
  );
