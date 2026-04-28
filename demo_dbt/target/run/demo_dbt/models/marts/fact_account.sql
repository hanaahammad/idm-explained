
  
    
    

    create  table
      "demo_dbt"."main"."fact_account__dbt_tmp"
  
    as (
      select
    a.agreement_sk,

    -- 🔥 CANONICAL CUSTOMER KEY
    'P' || LPAD(
        REGEXP_EXTRACT(CAST(acc.customer_id AS VARCHAR), '[0-9]+'),
        3,
        '0'
    ) as customer_key,

    acc.balance

from "demo_dbt"."main"."stg_core_accounts" acc
join "demo_dbt"."main"."core_agreement" a
    on acc.account_no = a.source_agreement_id
    );
  
  