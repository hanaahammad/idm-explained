select
    c.customer_key,
    c.name,
    COALESCE(SUM(a.balance), 0) as balance
from {{ ref('dim_customer') }} c
left join {{ ref('fact_account') }} a
    on c.customer_key = a.customer_key
group by c.customer_key, c.name