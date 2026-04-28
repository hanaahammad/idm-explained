
  
    
    

    create  table
      "demo_dbt"."main"."core_agreement__dbt_tmp"
  
    as (
      select
    row_number() over () as agreement_sk,
    account_no as source_agreement_id
from "demo_dbt"."main"."stg_core_accounts"
    );
  
  