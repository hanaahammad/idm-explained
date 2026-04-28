select
    row_number() over () as agreement_sk,
    account_no as source_agreement_id
from {{ ref('stg_core_accounts') }}