
  
    
    

    create  table
      "demo_dbt"."main"."dim_customer__dbt_tmp"
  
    as (
      SELECT
    party_id AS customer_key,
    name
FROM "demo_dbt"."main"."core_party"
WHERE party_type = 'PERSON'
    );
  
  