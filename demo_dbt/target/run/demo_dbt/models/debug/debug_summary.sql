
  
  create view "demo_dbt"."main"."debug_summary__dbt_tmp" as (
    -- models/debug/debug_summary.sql

SELECT
    COUNT(*) AS total_records,

    SUM(CASE WHEN p.party_id IS NULL THEN 1 ELSE 0 END) AS unmapped_records,

    ROUND(
        100.0 * SUM(CASE WHEN p.party_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS mapping_success_rate

FROM "demo_dbt"."main"."stg_core_accounts" s
LEFT JOIN "demo_dbt"."main"."party_identifier" p
    ON p.source_id = s.customer_id
  );
