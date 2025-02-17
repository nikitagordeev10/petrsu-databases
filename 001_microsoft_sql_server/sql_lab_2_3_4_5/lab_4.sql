SELECT 
	tblLesson.txtTheme AS 'Тема урока', 
	tblSubject.txtSubjectName AS 'Предмет', 
    tblLesson.datLessonDate AS 'Дата проведения' 
FROM 
	tblLesson, 
    tblSubject

WHERE 
	(tblLesson.intSubjectId = tblSubject.intSubjectId)

	and
	
	(tblSubject.txtSubjectName = 'математика' 
    or tblSubject.txtSubjectName = 'физика')
	
	and 

	((tblLesson.datLessonDate BETWEEN '01.01.2014' and '01.02.2014')
    or (tblLesson.datLessonDate BETWEEN '01.05.2014' and '01.06.2014'))	

ORDER BY 
	tblLesson.datLessonDate ASC