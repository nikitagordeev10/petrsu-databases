-- Написать команду добавления в таблицу use записей об использовании в количестве 10 штук всех неиспользуемых в проекте с номером 20 деталей.

INSERT INTO tblUse (id_project, id_detail, number)
SELECT 20, id_detail, 10
FROM tblDetail
WHERE id_detail NOT IN (
    SELECT id_detail
    FROM tblUse
    WHERE id_project = 20
);