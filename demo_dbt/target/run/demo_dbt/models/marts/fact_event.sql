
  
    
    

    create  table
      "demo_dbt"."main"."fact_event__dbt_tmp"
  
    as (
      select
    a.agreement_sk,
    e.event_type,
    e.event_date

from "demo_dbt"."main"."core_event" e

join "demo_dbt"."main"."core_agreement" a
    on REPLACE(CAST(e.agreement_id AS VARCHAR), 'A', '')
       = CAST(a.source_agreement_id AS VARCHAR)
    );
  
  