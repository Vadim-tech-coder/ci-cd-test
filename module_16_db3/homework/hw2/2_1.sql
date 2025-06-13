SELECT customer.full_name, manager.full_name, `order`.purchase_amount, `order`.date
FROM `order` JOIN customer ON `order`.customer_id = customer.customer_id
JOIN manager ON manager.manager_id = `order`.manager_id
ORDER BY `order`.date DESC