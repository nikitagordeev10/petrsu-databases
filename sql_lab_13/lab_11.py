import pyodbc
from fpdf import FPDF
import pandas as pd

def create_report_lab_11():
    pdf = FPDF('L')
    pdf.add_font('Arial', '', 'arial.ttf', uni=True)
    pdf.set_font('Arial', '', 9)

    connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10', database='master', user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')

    query = '''
    SELECT DISTINCT P.intPupilId, P.txtPupilSurname, P.txtPupilName, P.datBirthday, P.txtAddress
    FROM tblPupil AS P, tblMark AS M
    WHERE P.intPupilId = M.intPupilId
    ORDER BY P.txtPupilSurname, P.txtPupilName
    '''

    df_pupils = pd.read_sql(query, connection)


    pdf.add_page()

    for index, pupil in df_pupils.iterrows():
        pdf.multi_cell(0, 8, f"Фамилия: {pupil['txtPupilSurname']}\nИмя: {pupil['txtPupilName']}\nДата рождения: {pupil['datBirthday']}\nАдрес: {pupil['txtAddress']}\n", 0, 'L')

        pdf.cell(0, 0, "", border="B", ln=True) 
        pdf.cell(35, 8, txt="Название предмета", border=0, align='C')
        pdf.cell(35, 8, txt="Учитель", border=0, align='C')
        pdf.cell(15, 8, txt="Часы", border=0, align='C')
        pdf.cell(25, 8, txt="Дата урока", border=0, align='C')
        pdf.cell(60, 8, txt="Тема урока", border=0, align='C')
        pdf.cell(15, 8, txt="Оценка", border=0, align='C')
        pdf.cell(62, 8, txt="Замечания", border=0, align='C')
        pdf.cell(30, 8, txt="Средняя оценка", border=0, align='C')
        pdf.ln()
        pdf.cell(0, 0, "", border="B", ln=True) 
        pdf.ln()

        query_lessons = f'''
        SELECT S.txtSubjectName, T.txtTeacherName, S.intSubjectVolume, L.datLessonDate, L.txtTheme, M.intMarkValue, M.txtMarkComment
        FROM tblPupil AS P, tblMark AS M, tblLesson AS L, tblSubject AS S, tblTeacher AS T
        WHERE P.intPupilId = M.intPupilId 
        AND M.intLessonId = L.intLessonId 
        AND L.intSubjectId = S.intSubjectId 
        AND S.intTeacherId = T.intTeacherId 
        AND P.intPupilId = {pupil["intPupilId"]}
        ORDER BY S.txtSubjectName, L.datLessonDate
        '''

        df_lessons = pd.read_sql(query_lessons, connection)

        grouped_subjects = df_lessons.groupby('txtSubjectName')
        prev_subject = None # Инициализация переменной для предыдущего предмета
        for subject, subject_df in grouped_subjects:
            # Вывод оценок для конкретного предмета
            for _, lesson in subject_df.iterrows():
                avg_mark = round(subject_df['intMarkValue'].mean(), 2)
                teacher_name = lesson['txtTeacherName']
                name_parts = teacher_name.split(' ')
                formatted_name = f"{name_parts[1][:1]}. {name_parts[2][:1]}. {name_parts[0]}"
            
                start_y = pdf.get_y()
                
                # Проверка на изменение предмета
                if subject == prev_subject:
                    pdf.set_text_color(255, 255, 255) # Красный цвет для "Название предмета", "Учитель" и "Часы"
                
                pdf.cell(35, 8, txt=str(subject), border=0, align='C') # Убрать границы ячеек и выровнять текст по центру
                pdf.cell(35, 8, txt=str(formatted_name), border=0, align='C')
                pdf.cell(15, 8, txt=str(lesson["intSubjectVolume"]), border=0, align='C') # Убрать границы ячеек и выровнять текст по центру
                
                if subject == prev_subject:
                    pdf.set_text_color(0, 0, 0) # Черный цвет для остальных столбцов
                    
                pdf.cell(25, 8, txt=str(lesson["datLessonDate"]), border=0, align='C') # Убрать границы ячеек и выровнять текст по центру
                
                # Вывод комментария к теме урока
                comment_y_Theme = pdf.get_y()             
                pdf.set_y(start_y)
                pdf.set_x(pdf.get_x() - 187)
                pdf.multi_cell(60, 8, txt=str(lesson["txtTheme"]), border=0, align='C') # Убрать границы ячеек и выровнять текст по центру
                
                pdf.set_y(start_y)
                pdf.set_x(pdf.get_x() - 127)
                pdf.cell(15, 8, txt=str(lesson["intMarkValue"]), border=0, align='C') # Убрать границы ячеек и выровнять текст по центру
                
                # Вывод комментария к оценке
                comment_y_MarkComment = pdf.get_y() 
                pdf.set_y(start_y)
                pdf.set_x(pdf.get_x() - 112)
                pdf.multi_cell(62, 8, txt=str(lesson["txtMarkComment"]), border=0, align='C') # Убрать границы ячеек и выровнять текст по центру
                max_y = max(comment_y_MarkComment, pdf.get_y())
                
                pdf.set_y(start_y)
                pdf.set_x(257)        
                pdf.cell(30, 8, txt=str(avg_mark), border=0, align='C') # Убрать границы ячеек и выровнять текст по центру
                
                pdf.set_y(max_y)
                pdf.ln()
                
                prev_subject = subject # Обновление значения предыдущего предмета


            pdf.cell(0, -8, "", border="B", ln=True) # Добавить горизонтальную линию между строками
                

        total_marks = df_lessons['intMarkValue'].count()
        pdf.set_y(pdf.get_y()+8)
        pdf.multi_cell(0, 8, f"Количество оценок: {total_marks}", 0, 'L')
        pdf.ln()

        pdf.add_page()

    pdf.output("Ведомость.pdf")
