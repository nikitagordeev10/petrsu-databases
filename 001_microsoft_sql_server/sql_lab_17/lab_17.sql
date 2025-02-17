CREATE PROCEDURE spCreateReport -- cоздание процедуры 
    @ReportParam NVARCHAR(20) -- параметр отчета
AS
BEGIN
    IF OBJECT_ID('tempdb..#SchoolReport') IS NOT NULL -- проверка существования временной таблицы
        DROP TABLE #SchoolReport; -- если существует, то удаляется

    CREATE TABLE #SchoolReport ( -- создание временной таблицы 
        [Идентификатор предмета] INT,
        [Дата проведения урока] DATE,
        [Название предмета] NVARCHAR(20),
        [Тема урока] NVARCHAR(100),
        [Имя ученика] NVARCHAR(25),
        [Фамилия ученика] NVARCHAR(30),
        [Оценка, полученная учеником] INT
    );

    INSERT INTO #SchoolReport ([Идентификатор предмета], [Дата проведения урока], [Название предмета], [Тема урока], [Имя ученика], [Фамилия ученика], [Оценка, полученная учеником]) -- Заполнение временной таблицы
        SELECT 
            L.intLessonId as [Идентификатор предмета], 
            L.datLessonDate as [Дата проведения урока], 
            S.txtSubjectName as [Название предмета], 
            L.txtTheme as [Тема урока], 
            P.txtPupilName as [Имя ученика], 
            P.txtPupilSurname as [Фамилия ученика], 
            M.intMarkValue as [Оценка, полученная учеником]
        FROM 
            tblLesson L, 
            tblSubject S, 
            tblMark M, 
            tblPupil P
        WHERE 
            L.intSubjectId = S.intSubjectId 
            AND M.intPupilId = P.intPupilId 
            AND L.intLessonId = M.intLessonId
            AND S.txtSubjectName = @ReportParam; -- значение соответствует значению входного параметра @ReportParam
    
    SELECT * FROM #SchoolReport; -- вывод данных из временной таблицы
END; 

-- Выполнение хранимой процедуры
EXEC spCreateReport 'русский язык';

-- Удаление процедуры
DROP PROCEDURE spCreateReport;