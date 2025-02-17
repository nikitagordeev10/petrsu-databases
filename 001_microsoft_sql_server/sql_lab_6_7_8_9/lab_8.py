import tkinter as tk
import pyodbc

connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10', database='master',
                            user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')

# Функция для просмотра списка уроков
def view_lessons():
    # Создаем холст с полосой прокрутки
    canvas = tk.Canvas(lessons, bg='white')
    canvas.place(x=10, y=20, relwidth=0.96, height=520)
    scrollbar = tk.Scrollbar(lessons, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.place(relx=0.96, y=20, height=520)

    # Создаем фрейм для таблицы, используя холст в качестве родительского элемента
    table_container = tk.Frame(canvas, bg='white', bd=1, relief=tk.SOLID)
    canvas.create_window((0, 0), window=table_container, anchor=tk.NW)

    # Устанавливаем функцию привязки на изменение размера фрейма, чтобы наша полоса прокрутки была правильного размера
    table_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.configure(yscrollcommand=scrollbar.set)

    # Устанавливаем заголовки столбцов таблицы
    tk.Label(table_container, text="Название предмета", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=0, sticky="nsew")
    tk.Label(table_container, text="Дата проведения урока", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=1, sticky="nsew")
    tk.Label(table_container, text="Тема урока", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=2, sticky="nsew")
    tk.Label(table_container, text="ФИО преподавателя", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=3, sticky="nsew")

    # Определяем количество строк, необходимых для заполнения таблицы
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM tblLesson")
    num_rows = cursor.fetchone()[0]

    # Выполняем запрос на выборку данных из трех таблиц базы данных
    cursor.execute("""
        SELECT 
            tblSubject.txtSubjectName, 
            tblLesson.datLessonDate, 
            tblLesson.txtTheme, 
            tblTeacher.txtTeacherName,
            tblLesson.intLessonId
        FROM 
            tblSubject, tblTeacher, tblLesson
        WHERE 
            (tblSubject.intSubjectId = tblLesson.intSubjectId) and (tblSubject.intTeacherId = tblTeacher.intTeacherId)
            and tblLesson.intLessonId BETWEEN 1 AND ?
        """, (num_rows,))

    rows = cursor.fetchall()

    # Отображаем полученную информацию в таблице
    for i, row in enumerate(rows):
        for j, value in enumerate(row[:-1]):
            tk.Label(table_container, text=value, bd=1, bg='white', relief=tk.SOLID).grid(row=i+1, column=j, sticky="nsew")
        # Кнопка в соответствующем поле "Тема урока"
        tk.Button(table_container, text=row[2], bg="white", command=lambda lesson_id=row[-1]: open_lesson_details(lesson_id)).grid(row=i+1, column=2, sticky="nsew")


# Окно для просмотра данных об одном уроке
def open_lesson_details(lesson_id):
    window = tk.Toplevel()
    window.title("Урок")
    window.geometry("800x500")
    window.configure(bg="#F0F0F0")

    canvas = tk.Canvas(window, bg='white')
    canvas.place(x=10, y=20, relwidth=0.96, height=400)
    scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.place(relx=0.96, y=20, height=450)

    global details_container
    details_container = tk.Frame(canvas, bg='white', bd=1, relief=tk.SOLID)
    canvas.create_window((0, 0), window=details_container, anchor=tk.NW)
    details_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.configure(yscrollcommand=scrollbar.set)

    # Заголовки столбцов таблицы
    tk.Label(details_container, text="Фамилия ученика", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=0, sticky="nsew")
    tk.Label(details_container, text="Имя ученика", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=1, sticky="nsew")
    tk.Label(details_container, text="Дата рождения ученика", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=2, sticky="nsew")
    tk.Label(details_container, text="Оценка", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=3, sticky="nsew")
    tk.Label(details_container, text="Замечания", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=4, sticky="nsew")

    view_lesson_details(lesson_id)

    # Кнопки "Отмена" и "Добавить урок"
    cancel_button = tk.Button(window, text="Отмена", command=window.destroy)
    cancel_button.place(x=100, y=450)

def view_lesson_details(lesson_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 
            tblPupil.txtPupilSurname, 
            tblPupil.txtPupilName, 
            tblPupil.datBirthday, 
            tblMark.intMarkValue,
            tblMark.txtMarkComment
        FROM 
            tblMark, tblPupil
        WHERE 
            tblMark.intLessonId = ?
            AND tblPupil.intPupilId = tblMark.intPupilId
    """, (lesson_id,))

    rows = cursor.fetchall()
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            tk.Label(details_container, text=value, bd=1, bg='white', relief=tk.SOLID).grid(row=i+1, column=j, sticky="nsew")


# ================================================
lessons = tk.Tk()
lessons.title("Уроки")
lessons.geometry("950x600")
lessons.configure(bg="#F0F0F0")

# Выводим список уроков в таблице
view_lessons()


lessons.mainloop()