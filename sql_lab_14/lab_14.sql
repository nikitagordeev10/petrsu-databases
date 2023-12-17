CREATE TRIGGER trg_check_double_marks -- триггер, проверяет наличие двух одинаковых оценок для одного ученика по одному предмету в один и тот же день 
ON tblMark
AFTER INSERT -- после вставки новой строки в tblMark
AS
BEGIN
    IF EXISTS ( -- есть ли две одинаковые оценки?
        SELECT 1 -- выбирает константу или false
        FROM 
            tblMark m1, 
            tblLesson l1, 
            tblSubject s1, 
            INSERTED i, -- оценки, которые были только что вставлены
            tblLesson l2, 
            tblSubject s2
        WHERE m1.intLessonId = l1.intLessonId -- присоединяем таблицы
          AND s1.intSubjectId = l1.intSubjectId -- присоединяем таблицы
          AND i.intPupilId = m1.intPupilId -- присоединяем таблицы
          AND l2.intLessonId = i.intLessonId -- присоединяем таблицы
          AND s2.intSubjectId = l2.intSubjectId -- присоединяем таблицы
          AND s1.intSubjectId = s2.intSubjectId -- проверяем, что предметы совпадают
          AND l1.datLessonDate = l2.datLessonDate -- проверяем, что даты занятий совпадают
          AND m1.intMarkId <> i.intMarkId -- исключаем дублирование записей
    )
    BEGIN -- если найдены записи
        RAISERROR('Ученик не может получить две оценки по одному предмету в один день', 16, 1); -- выводим сообщение об ошибке
        ROLLBACK TRANSACTION; -- отменяем изменения
    END;
END;
GO

-- Проверка работы триггера 
-- добавление двух оценок на одну дату 
INSERT INTO tblMark (intLessonId, intPupilId, intMarkValue, txtMarkComment) VALUES (3, 1, 5, 'Хорошо');
INSERT INTO tblMark (intLessonId, intPupilId, intMarkValue, txtMarkComment) VALUES (3, 1, 4, 'Неплохо');

-- Удаление триггера
SELECT * FROM sys.triggers;
DROP TRIGGER trg_check_double_marks;
