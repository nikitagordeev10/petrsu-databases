CREATE TRIGGER trg_insert_lesson -- триггер, для увеличения количества проведенных уроков после добавления нового урока
ON tblLesson
AFTER INSERT -- автоматически запускается после вставки 
AS
BEGIN
  UPDATE tblSubject -- обновляем записи в таблице  
  SET intLessonCount = intLessonCount + 1 -- увеличиваем количество уроков в таблице на 1
  WHERE tblSubject.intSubjectId IN (SELECT INSERTED.intSubjectId FROM INSERTED) -- сопоставляем записи добавленного урока и предмета
END


CREATE TRIGGER trg_delete_lesson -- триггер, для уменьшения количества проведенных уроков после удаления урока
ON tblLesson
AFTER DELETE -- автоматически запускающийся после удаления
AS
BEGIN
  UPDATE tblSubject -- обновляет записи в таблице  
  SET intLessonCount = intLessonCount - 1 -- уменьшаем количество уроков в таблице на 1
  WHERE tblSubject.intSubjectId IN (SELECT DELETED.intSubjectId FROM DELETED) -- сопоставляем записи удаленного урока и предмета
END


-- Проверка триггера 
INSERT INTO tblLesson (intSubjectId, datLessonDate, txtTheme) -- урок
VALUES (31, '2021-11-01', 'Тема урока 1');

SELECT * FROM tblSubject; -- проверим, что количество проведенных уроков изменилось на 1:

DELETE FROM tblLesson WHERE intSubjectId = 32; -- удалим урок и проверим, что количество проведенных уроков вернулось к 0:
SELECT * FROM tblSubject;


-- Удаление триггера 
SELECT * FROM sys.triggers;
DROP TRIGGER trg_insert_lesson;
DROP TRIGGER trg_delete_lesson;