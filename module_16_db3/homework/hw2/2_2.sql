SELECT c.full_name
FROM customer c
LEFT JOIN "order" o ON o.customer_id = c.customer_id
WHERE o.customer_id IS NULL
ORDER BY full_name