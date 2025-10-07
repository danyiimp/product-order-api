-- Написать текст запроса для отчета (view) 
-- «Топ-5 самых покупаемых товаров за последний месяц» 
-- (по количеству штук в заказах). 
-- В отчете должны быть: Наименование товара, 
-- Категория 1-го уровня, Общее количество проданных штук

CREATE OR REPLACE VIEW top_5_best_selling_products AS (
	WITH RECURSIVE category_with_root AS (
		SELECT id, name, name AS root_name
		FROM category
		WHERE parent_id IS NULL
	
		UNION ALL
	
		SELECT c.id, c.name, cwr.root_name
		FROM category AS c
		JOIN category_with_root AS cwr 
		ON c.parent_id = cwr.id	
	)

	SELECT 
		item.name, 
		cwr.root_name AS "root_category", 
		SUM(order_item.quantity) AS "total_sold"
	FROM item
	JOIN category_with_root AS cwr ON item.category_id = cwr.id
	JOIN order_item ON item.id = order_item.item_id
	JOIN "order" ON order_item.order_id = "order".id 
	WHERE DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE)
	GROUP BY item.id, item.name, cwr.root_name
	ORDER BY "total_sold" DESC
	LIMIT 5
);


SELECT *
FROM top_5_best_selling_products
