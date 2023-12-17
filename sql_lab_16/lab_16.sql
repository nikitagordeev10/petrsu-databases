CREATE PROCEDURE spGetPupilSubjectMarks -- cоздание процедуры 
AS
BEGIN
    IF OBJECT_ID('tempdb..#PupilSubjectMarks') IS NOT NULL -- удаляем временную таблицу, если она существует
        DROP TABLE #PupilSubjectMarks;

    CREATE TABLE #PupilSubjectMarks ( -- cоздаем временную таблицу для хранения данных с измененными названиями столбцов
        [ФИО ученика] NVARCHAR(55) NOT NULL, 
        [Название предмета] NVARCHAR(20) NOT NULL, 
        [Количество полученных оценок по предмету] INT NOT NULL 
    );

    INSERT INTO #PupilSubjectMarks ([ФИО ученика], [Название предмета], [Количество полученных оценок по предмету]) -- наполняем временную таблицу данными
        SELECT 
			p.txtPupilSurname + ' ' + p.txtPupilName AS [ФИО ученика],
			s.txtSubjectName AS [Название предмета],
			COUNT(m.intMarkId) AS [Количество полученных оценок по предмету]
		FROM 
			tblPupil p,
			tblSubject s,
			tblLesson l,
			tblMark m
		WHERE 
			p.intPupilId = m.intPupilId AND 
			l.intLessonId = m.intLessonId AND 
			l.intSubjectId = s.intSubjectId
		GROUP BY 
			p.txtPupilSurname,
			p.txtPupilName,
			s.txtSubjectName
		ORDER BY 
			p.txtPupilSurname;

    
    SELECT [ФИО ученика], [Название предмета], [Количество полученных оценок по предмету] FROM #PupilSubjectMarks; -- Выводим результат
END;

-- Проверка работы созданной процедуры:
EXEC spGetPupilSubjectMarks;

-- Удаление процедуры
DROP PROCEDURE spGetPupilSubjectMarks;