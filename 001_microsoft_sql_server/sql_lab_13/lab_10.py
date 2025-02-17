import pyodbc
import pandas as pd
from fpdf import FPDF

def create_report_lab_10():
    # Установка шрифтов
    pdf = FPDF()
    pdf.add_font('Arial', '', 'arial.ttf', uni=True)
    pdf.set_font('Arial')

    # Подключение к БД
    connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10', database='master', user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')
    cursor = connection.cursor()

    # Получение списка учителей
    cursor.execute("SELECT intTeacherId, txtTeacherName, intTeacherYear, fltTeacherSalary FROM tblTeacher")
    teachers = []
    for row in cursor.fetchall():
        teacher = dict(id=row[0], name=row[1], year=row[2], salary=row[3])
        teachers.append(teacher)

    # Переменные для хранения отступов
    top_margin = 10
    bottom_margin = 10

    # Создание новой страницы
    pdf.add_page()

    # Текущая координата Y на странице
    current_y = pdf.get_y()

    # Перебор учителей
    for teacher in teachers:
        # Получение списка предметов, которые ведет учитель
        cursor.execute(f"SELECT txtSubjectName, intSubjectVolume, intLessonCount FROM tblSubject WHERE intTeacherId = {teacher['id']}")
        subjects = []
        for row in cursor.fetchall():
            subject = dict(name=row[0], volume=row[1], lesson_count=row[2])
            subjects.append(subject)

        # Расчет переменной высоты блока информации об учителе
        block_height = (len(subjects) * 10) + 70

        # Проверка наличия достаточного количества места на странице
        available_height = pdf.h - current_y - bottom_margin

        # Вывод ФИО, года принятия на работу и оклада при создании новой страницы
        if available_height < block_height:
            pdf.add_page()
            current_y = pdf.get_y()
            pdf.multi_cell(0, 10, f'ФИО: {teacher["name"]}\nГод принятия на работу: {teacher["year"]}\nОклад: {teacher["salary"]}\n', 0, 'L') 

        # Вывод ФИО, года принятия на работу и оклада при новом учителе
        if current_y == pdf.get_y():
            pdf.multi_cell(0, 10, f'ФИО: {teacher["name"]}\nГод принятия на работу: {teacher["year"]}\nОклад: {teacher["salary"]}\n', 0, 'L')

        # Вывод списка предметов
        pdf.cell(50, 10, "Название предмета", border=1)
        pdf.cell(50, 10, "Количество часов", border=1)
        pdf.cell(80, 10, "Количество проведённых уроков", border=1)
        pdf.ln()
        for subject in subjects:
            pdf.cell(50, 10, str(subject["name"]), border=1)
            pdf.cell(50, 10, str(subject["volume"]), border=1)
            pdf.cell(80, 10, str(subject["lesson_count"]), border=1)
            pdf.ln()

        # Вывод суммарного количества предметов и часов
        total_subjects = len(subjects)
        total_hours = sum([subject["volume"] for subject in subjects])
        pdf.multi_cell(0, 10, f'Количество предметов: {total_subjects}\nКоличество часов: {total_hours}', 0, 'L')

        # Отделение информации об учителе горизонтальной чертой
        pdf.cell(0, 4, "", border="B", ln=True)
        pdf.cell(0, 4, "", ln=True) 

        # Изменение текущей координаты Y на странице
        current_y = pdf.get_y() 

    # Вывод информации о количестве учителей в отчете
    pdf.add_page()
    pdf.cell(0, 10, txt=f"Количество учителей: {len(teachers)}", ln=True)

    pdf.output("Учителя.pdf")
