-- Написать в правильном порядке команды удаления всех записей базы данных, связанных с деталью под номером 5, при условии отсутствия каскадного удаления.

DELETE FROM tblUse WHERE id_detail = 5;
DELETE FROM tblDelivery WHERE id_detail = 5;
DELETE FROM tblDetail WHERE id_detail = 5;