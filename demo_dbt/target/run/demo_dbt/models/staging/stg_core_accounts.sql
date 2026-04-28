
  
  create view "demo_dbt"."main"."stg_core_accounts__dbt_tmp" as (
    SELECT * FROM "demo_dbt"."main"."core_banking_accounts"
  );
