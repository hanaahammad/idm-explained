select
    a.agreement_sk,
    e.event_type,
    e.event_date

from {{ ref('core_event') }} e

join {{ ref('core_agreement') }} a
    on REPLACE(CAST(e.agreement_id AS VARCHAR), 'A', '')
       = CAST(a.source_agreement_id AS VARCHAR)