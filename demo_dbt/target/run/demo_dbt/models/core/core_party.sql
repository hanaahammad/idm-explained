
  
    
    

    create  table
      "demo_dbt"."main"."core_party__dbt_tmp"
  
    as (
      SELECT 'P001' AS party_id, 'Alice Smith' AS name, 'PERSON' AS party_type
UNION ALL
SELECT 'P002', 'Bob Martin', 'PERSON'
UNION ALL
SELECT 'P003', 'Charlie Lee', 'PERSON'
UNION ALL
SELECT 'P_BANK', 'MyBank', 'ORGANIZATION'
    );
  
  