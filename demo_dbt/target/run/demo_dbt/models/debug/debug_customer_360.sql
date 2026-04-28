
  
  create view "demo_dbt"."main"."debug_customer_360__dbt_tmp" as (
    select
    c.customer_key,
    c.name,
    max(a.customer_key) as fact_customer_key,
    sum(a.balance) as balance,

    case 
        when max(a.customer_key) is not null then 'MATCH'
        else 'NO MATCH'
    end as join_status

from "demo_dbt"."main"."dim_customer" c

left join "demo_dbt"."main"."fact_account" a
    on c.customer_key = a.customer_key

group by c.customer_key, c.name
  );
