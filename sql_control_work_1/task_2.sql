-- Получить ФИО сотрудника, его разряд, название проекта, в котором он участвует, и его зарплату в этом проекте. Упорядочить по убыванию зарплаты, по возрастанию названия проекта, по возрастанию ФИО.

SELECT w.name as 'ФИО сотрудника', w.spec as 'Разряд', p.name as 'Название проекта', pr.salary as 'Зарплата в проекте'
FROM tblWorker as w, tblParticipate as pr, tblProject as p
WHERE w.id_worker = pr.id_worker AND pr.id_project = p.id_project
ORDER BY pr.salary DESC, p.name ASC, w.name ASC;