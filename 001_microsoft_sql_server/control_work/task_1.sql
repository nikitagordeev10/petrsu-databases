-- Получить информацию (включающую идентификатор поставки и объем поставки) о поставках, выполняемых в объеме не менее 200 штук, поставщиками с идентификаторами 20 или 21, или 22. Упорядочить по убыванию объема поставки, по убыванию идентификатора.

SELECT id_delivery as 'Идентификатор поставки', number as 'Объем поставки'
FROM tblDelivery
WHERE id_provider IN (20, 21, 22) AND number >= 200
ORDER BY number DESC, id_delivery DESC;