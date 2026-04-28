
  
  create view "demo_dbt"."main"."stg_crm_customers__dbt_tmp" as (
    SELECT * FROM "demo_dbt"."main"."crm_customers"
  );
