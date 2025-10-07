-- Найти количество дочерних элементов первого 
-- уровня вложенности для категорий номенклатуры.

SELECT c1.name, COUNT(*)
FROM category AS c1
JOIN category AS c2 ON c2.parent_id = c1.id
WHERE c1.parent_id IS NULL
GROUP BY c1.id, c1.name