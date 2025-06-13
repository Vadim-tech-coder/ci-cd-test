SELECT c1.full_name AS 'Покупатель 1',
		c2.full_name AS 'Покупатель 2',
  		c1.city, c2.city,
  		c1.manager_id, c2.manager_id
 FROM customer c1
 CROSS JOIN customer c2
 ON c1.customer_id = c2.customer_id
 WHERE c1.city = c2.city
 AND c1.manager_id = c2.manager_id