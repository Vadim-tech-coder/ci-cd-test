SELECT o.order_no, c.full_name
FROM 'order' o
JOIN customer c  ON c.customer_id = o.customer_id
WHERE o.manager_id IS NULL