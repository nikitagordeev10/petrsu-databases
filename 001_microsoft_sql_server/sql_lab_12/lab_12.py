from fpdf import FPDF
import pyodbc


# Функция для извлечения информации из базы данных
def fetch_data(subject_name):
    query = f"""
        SELECT P.txtPupilSurname, P.txtPupilName, M.intMarkValue, T.txtTeacherName, S.intSubjectVolume, L.datLessonDate, L.txtTheme
        FROM tblMark AS M, tblPupil AS P, tblLesson AS L, tblSubject AS S, tblTeacher AS T
        WHERE M.intPupilId = P.intPupilId
        AND M.intLessonId = L.intLessonId
        AND L.intSubjectId = S.intSubjectId
        AND S.intTeacherId = T.intTeacherId
        AND S.txtSubjectName = '{subject_name}'
        ORDER BY L.datLessonDate DESC;
        """

    connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10',
                                database='master', user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data


# Функция для создания отчета
def create_report(subject_name):
    data = fetch_data(subject_name)

    if not data:
        print("Не найдено данных для данного предмета")
        return

    teacher_name, subject_hours, report_title = None, None, None
    lesson_data = {}

    for row in data:
        pupil_name = f"{row[0]} {row[1]}"
        mark = row[2]
        teacher_name = row[3]
        subject_hours = row[4]
        lesson_date = row[5]
        lesson_theme = row[6]

        if not report_title:
            report_title = f"Школьный журнал: {subject_name}"

        if lesson_date not in lesson_data:
            lesson_data[lesson_date] = {
                "theme": lesson_theme,
                "marks": []
            }

        lesson_data[lesson_date]["marks"].append((pupil_name, mark))

    lesson_data = dict(sorted(lesson_data.items(), reverse=True))

    pdf = FPDF()
    pdf.add_page()

    # Установка шрифта
    pdf.add_font('Arial', '', 'arial.ttf', uni=True)
    pdf.set_font('Arial', '', 12)

    # Заголовок отчета
    pdf.cell(0, 10, report_title, 0, 1, 'C')

    # Данные о предмете
    pdf.multi_cell(0, 10, f"ФИО учителя: {teacher_name}\nКоличество часов: {subject_hours}", 0, 1, 'L')

    # Данные о занятиях
    for lesson_date, lesson_item in lesson_data.items():
        pdf.multi_cell(0, 10, f"Дата проведения урока: {lesson_date}\nТема урока:{lesson_item['theme']}", 0, 1, 'L')

        lesson_marks = [(student[0], student[1]) for student in lesson_item["marks"]]

        # Создание таблицы с оценками
        pdf.cell(80, 10, "Ученик", 1)
        pdf.cell(20, 10, "Оценка", 1)
        pdf.ln()

        for pupil_name, mark in lesson_marks:
            pdf.cell(80, 10, pupil_name, 1)
            pdf.cell(20, 10, str(mark), 1)
            pdf.ln()

    pdf.output("Школьный журнал.pdf")  # Сохранение PDF-файла


# Создание отчета
subject_name = "русский язык"  # Здесь введите название предмета, для которого хотите создать отчет
create_report(subject_name)
