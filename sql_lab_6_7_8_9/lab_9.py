import tkinter as tk
import pyodbc

connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10', database='master',
                            user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')

# Функция для просмотра списка уроков
def view_lessons():
    canvas = tk.Canvas(lessons, bg='white')
    canvas.place(x=10, y=20, relwidth=0.96, height=520)
    scrollbar = tk.Scrollbar(lessons, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.place(relx=0.96, y=20, height=520)

    table_container = tk.Frame(canvas, bg='white', bd=1, relief=tk.SOLID)
    canvas.create_window((0, 0), window=table_container, anchor=tk.NW)

    table_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.configure(yscrollcommand=scrollbar.set)

    tk.Label(table_container, text="Название предмета", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=0, sticky="nsew")
    tk.Label(table_container, text="Дата проведения урока", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=1, sticky="nsew")
    tk.Label(table_container, text="Тема урока", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=2, sticky="nsew")
    tk.Label(table_container, text="ФИО преподавателя", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=3, sticky="nsew")

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM tblLesson")
    num_rows = cursor.fetchone()[0]

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
    add_lesson_button = tk.Button(window, text="Новая оценка", command=lambda: open_new_mark(lesson_id, window))
    add_lesson_button.place(x=600, y=450)


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


def open_new_mark(lesson_id, window_open_lesson_details):
       
    new_mark_window = tk.Toplevel()
    new_mark_window.title("Новая оценка")
    new_mark_window.geometry("950x750")
    new_mark_window.configure(bg="#F0F0F0")

    # Используем SELECT-запрос, чтобы получить информацию о нужном уроке
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 
            tblSubject.txtSubjectName, 
            tblLesson.datLessonDate, 
            tblLesson.txtTheme
        FROM 
            tblSubject, tblLesson
        WHERE 
            (tblSubject.intSubjectId = tblLesson.intSubjectId)
            AND (tblLesson.intLessonId = ?)
        """, (lesson_id,))
    
    subject_name, lesson_date, theme = cursor.fetchone()

    # Добавляем разделитель перед информацией об уроке
    separator_top = tk.Frame(new_mark_window, height=2, bg="black")
    separator_top.place(relx=0.01, y=10, relwidth=0.6)

    # Создание и размещение названия предмета, даты урока и названия темы
    tk.Label(new_mark_window, text=f"Предмет: {subject_name}", bg="#F0F0F0", font=("Arial", 14)).place(x=10, y=30)
    tk.Label(new_mark_window, text=f"Дата урока: {lesson_date}", bg="#F0F0F0", font=("Arial", 14)).place(x=10, y=60)
    tk.Label(new_mark_window, text=f"Тема урока: {theme}", bg="#F0F0F0", font=("Arial", 14)).place(x=10, y=90)

    # Добавляем разделитель после информации об уроке
    separator_bottom = tk.Frame(new_mark_window, height=2, bg="black")
    separator_bottom.place(relx=0.01, y=130, relwidth=0.6)

    # Создание и размещение элементов интерфейса для ввода данных новой оценки
    tk.Label(new_mark_window, text="Ученик:", font=("Arial", 14)).place(x=10, y=180)
    cursor = connection.cursor()
    cursor.execute("SELECT txtPupilSurname, txtPupilName FROM tblPupil")
    pupils = cursor.fetchall()
    pupils_list = [f"{surname} {name}" for surname, name in pupils]
    pupil_var = tk.StringVar(new_mark_window)
    pupil_var.set(pupils_list[0])
    tk.OptionMenu(new_mark_window, pupil_var, *pupils_list).place(x=150, y=180)

    tk.Label(new_mark_window, text="Оценка:", font=("Arial", 14)).place(x=10, y=220)
    mark_var = tk.StringVar(new_mark_window)
    mark_var.set("5")
    tk.OptionMenu(new_mark_window, mark_var, "5", "4", "3", "2").place(x=150, y=220)

    tk.Label(new_mark_window, text="Замечания:", font=("Arial", 14)).place(x=10, y=260)
    comment_entry = tk.Entry(new_mark_window, font=("Arial", 14), width=50)
    comment_entry.place(x=150, y=260)

   # Кнопки "Отмена" и "Добавить урок"
    cancel_button = tk.Button(new_mark_window, text="Отмена", command=new_mark_window.destroy)
    cancel_button.place(x=220, y=500)
    add_lesson_button = tk.Button(new_mark_window, text="Добавить урок", command=lambda: submit_mark(lesson_id, pupil_var, mark_var, comment_entry, new_mark_window, window_open_lesson_details))
    add_lesson_button.place(x=620, y=500)


def submit_mark(lesson_id, pupil_var, mark_var, comment_entry, new_mark_window, window_open_lesson_details):
    # Получаем значения из элементов интерфейса
    pupil_var = pupil_var.get()
    pupil_surname, pupil_name = pupil_var.split(" ")
    
    cursor = connection.cursor()
    cursor.execute("""
        SELECT intPupilId
        FROM tblPupil
        WHERE txtPupilName = ? AND txtPupilSurname = ? 
    """, (pupil_name, pupil_surname))
    pupil_id = cursor.fetchone()[0]

    mark_value = mark_var.get()
    mark_comment = comment_entry.get()

    # Добавляем информацию об оценке в базу данных
    cursor.execute("""
        INSERT INTO tblMark (intLessonId, intPupilId, intMarkValue, txtMarkComment)
        VALUES (?, ?, ?, ?)
    """, (lesson_id, pupil_id, mark_value, mark_comment))

    connection.commit()

    new_mark_window.destroy()
    window_open_lesson_details.destroy()
    open_lesson_details(lesson_id)


lessons = tk.Tk()
lessons.title("Уроки")
lessons.geometry("950x600")
lessons.configure(bg="#F0F0F0")

# Выводим список уроков в таблице
view_lessons()

lessons.mainloop()