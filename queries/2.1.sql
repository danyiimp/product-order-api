-- Получение информации о сумме товаров заказанных 
-- под каждого клиента (Наименование клиента, сумма) 

SELECT customer.name, SUM(order_item.quantity * price)
FROM "order"
JOIN customer ON customer.id = customer_id
JOIN order_item ON "order".id = order_item.order_id
JOIN item ON item_id = item.id 
GROUP BY customer_id, customer.name
