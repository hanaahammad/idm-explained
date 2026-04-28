
  
    
    

    create  table
      "demo_dbt"."main"."customer_360__dbt_tmp"
  
    as (
      select
    c.customer_key,
    c.name,
    COALESCE(SUM(a.balance), 0) as balance
from "demo_dbt"."main"."dim_customer" c
left join "demo_dbt"."main"."fact_account" a
    on c.customer_key = a.customer_key
group by c.customer_key, c.name
    );
  
  