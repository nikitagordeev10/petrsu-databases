-- Получить имена поставщиков, поставляющих максимальное количество деталей. Упорядочить по возрастанию.

SELECT p.name AS 'Имя поставщика', COUNT(d.id_detail) AS 'Количество деталей'
FROM tblProvider p, tblDelivery d
WHERE p.id_provider = d.id_provider 
GROUP BY p.name
ORDER BY COUNT(d.id_detail) DESC, p.name ASC
LIMIT 1;