# Импортируем необходимые модули
import tkinter as tk
import pyodbc

# Подключение к базе данных SQL Server
connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10', database='master', user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')

# Функция по созданию таблицы с данными о предметах и кнопками для открытия окна с подробной информацией о каждом из них
def view_lessons():
    canvas = tk.Canvas(lessons, bg='white') # создаем новый холст с белым фоном
    canvas.place(x=10, y=20, relwidth=0.96, height=520) # устанавливаем параметры для холста
    scrollbar = tk.Scrollbar(lessons, orient=tk.VERTICAL, command=canvas.yview) # создаем вертикальный скроллбар
    scrollbar.place(relx=0.96, y=20, height=520) # устанавливаем параметры для скроллбара

    table_container = tk.Frame(canvas, bg='white', bd=1, relief=tk.SOLID) # создаем контейнер для таблицы
    canvas.create_window((0, 0), window=table_container, anchor=tk.NW) # создаем окно внутри холста и помещаем в него контейнер

    table_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all'))) # устанавливаем параметры контейнера
    canvas.configure(yscrollcommand=scrollbar.set) # настраиваем скроллбар

    # Создаем заголовки для столбцов таблицы
    tk.Label(table_container, text="Название предмета", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=0, sticky="nsew")
    tk.Label(table_container, text="Дата проведения урока", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=1, sticky="nsew")
    tk.Label(table_container, text="Тема урока", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=2, sticky="nsew")
    tk.Label(table_container, text="ФИО преподавателя", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=3, sticky="nsew")

    cursor = connection.cursor() # подключаемся к базе данных
    cursor.execute("SELECT COUNT(*) FROM tblLesson") # подсчитываем количество строк в таблице tblLesson
    num_rows = cursor.fetchone()[0] # получаем количество строк в таблице

    # Запрос для выборки данных из нескольких таблиц
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
        """, (num_rows,)) # выбираем данные из трех таблиц и устанавливаем параметры для WHERE

    rows = cursor.fetchall() # получаем все данные из запроса и записываем их в переменную rows

    # Создаем для каждой строки таблицы ячейки с данными и кнопкой для открытия подробной информации
    for i, row in enumerate(rows):
        for j, value in enumerate(row[:-1]):
            if j == 2:
                tk.Label(table_container, text=value, bd=1, bg='white', relief=tk.SOLID, fg='white').grid(row=i+1, column=j, sticky="nsew")
            else:
                tk.Label(table_container, text=value, bd=1, bg='white', relief=tk.SOLID).grid(row=i+1, column=j, sticky="nsew")

        # Кнопка в соответствующем поле "Тема урока"
        tk.Button(table_container, text=row[2], bg="white", command=lambda lesson_id=row[-1]: open_lesson_details(lesson_id)).grid(row=i+1, column=2, sticky="w")
        
# Функция добавления нового урока
def add_lesson():
    # Создаем дочернее окно для добавления урока
    new_lesson_window = tk.Toplevel()
    new_lesson_window.title("Новый урок")
    new_lesson_window.geometry("800x600")
    new_lesson_window.configure(bg="#F0F0F0")

    # Рамка для содержимого формы
    content_frame = tk.Frame(new_lesson_window, bg="#ABABAB", bd=2, relief="groove")
    content_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)

    # Добавляем варианты выбора предмета
    subject_label = tk.Label(content_frame, bg="#ABABAB",text="Название предмета")
    subject_label.place(relx=0.05, rely=0.05)

    # Заполнение выпадающего списка названий предметов из таблицы tblSubject
    subject_list = []
    cursor_subject = connection.cursor()
    cursor_subject.execute("SELECT txtSubjectName FROM tblSubject")
    for row in cursor_subject:
        subject_list.append(row[0])
    subject_name = tk.StringVar(content_frame)
    subject_name.set(subject_list[0])
    subject_dropdown = tk.OptionMenu(content_frame, subject_name, *subject_list)
    subject_dropdown.place(relx=0.5, rely=0.05)

    # Дата проведения урока
    date_label = tk.Label(content_frame, bg="#ABABAB", text="Дата проведения урока (yyyy-mm-dd)")
    date_label.place(relx=0.05, rely=0.25)
    date_entry = tk.Entry(content_frame)
    date_entry.place(relx=0.5, rely=0.25)

    # Тема урока
    theme_label = tk.Label(content_frame, bg="#ABABAB", text="Тема урока")
    theme_label.place(relx=0.05, rely=0.45)
    theme_entry = tk.Entry(content_frame)
    theme_entry.place(relx=0.5, rely=0.45)

    # ФИО преподавателя
    teacher_label = tk.Label(content_frame, bg="#ABABAB", text="ФИО преподавателя")
    teacher_label.place(relx=0.05, rely=0.65)

    # Заполнение выпадающего списка ФИО преподавателей из таблицы tblTeacher
    teacher_list = []
    cursor_teacher = connection.cursor()
    cursor_teacher.execute("SELECT txtTeacherName FROM tblTeacher")
    for row in cursor_teacher:
        teacher_list.append(row[0])
    teacher_name = tk.StringVar(content_frame)
    teacher_name.set(teacher_list[0])
    teacher_dropdown = tk.OptionMenu(content_frame, teacher_name, *teacher_list)
    teacher_dropdown.place(relx=0.5, rely=0.65)

    # Кнопки "Отмена" и "Добавить урок"
    cancel_button = tk.Button(new_lesson_window, text="Отмена", command=new_lesson_window.destroy)
    cancel_button.place(relx=0.2, rely=0.8)
    add_lesson_button = tk.Button(new_lesson_window, text="Добавить урок", command=lambda: add_lesson_to_database(subject_name, date_entry, theme_entry, teacher_name, subject_list, teacher_list))
    add_lesson_button.place(relx=0.6, rely=0.8)

# Функция добавления нового урока в базу данных
def add_lesson_to_database(subject_name, date_entry, theme_entry, teacher_name, subject_list, teacher_list):
    # Получаем значения выбранных опций и введенных значений
    subject = subject_name.get()
    date = date_entry.get()
    theme = theme_entry.get()
    teacher = teacher_name.get()

    # Получаем id выбранных предмета и преподавателя
    cursor_insert = connection.cursor()
    cursor_insert.execute("SELECT intSubjectId FROM tblSubject WHERE txtSubjectName = ?", (subject,))
    subject_id = cursor_insert.fetchone()[0]
    cursor_insert.execute("SELECT intTeacherId FROM tblTeacher WHERE txtTeacherName = ?", (teacher,))
    teacher_id = cursor_insert.fetchone()[0]

    # Добавляем новый урок в базу данных и связываем его с предметом
    cursor_insert.execute("INSERT INTO tblLesson (intSubjectId, datLessonDate, txtTheme) OUTPUT inserted.intLessonId VALUES (?, ?, ?)", (subject_id, date, theme))
    cursor_insert.execute("UPDATE tblSubject SET intTeacherId = ? WHERE intSubjectId = ?", (teacher_id, subject_id))
    connection.commit()

    # Очищаем поля ввода и устанавливаем значения опций по умолчанию
    subject_name.set(subject_list[0])
    date_entry.delete(0, tk.END)
    theme_entry.delete(0, tk.END)
    teacher_name.set(teacher_list[0])

    view_lessons()

# Функция для открытия окна с данными об одном уроке по его ID
def open_lesson_details(lesson_id):
    # Создание нового окна
    window = tk.Toplevel()
    window.title("Урок")
    window.geometry("800x500")
    window.configure(bg="#F0F0F0")

    # Создание холста для таблицы с данными
    canvas = tk.Canvas(window, bg='white')
    canvas.place(x=10, y=20, relwidth=0.96, height=400)
    scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.place(relx=0.96, y=20, height=450)

    # Создание контейнера для данных и привязка его к холсту
    global details_container
    details_container = tk.Frame(canvas, bg='white', bd=1, relief=tk.SOLID)
    canvas.create_window((0, 0), window=details_container, anchor=tk.NW)
    details_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.configure(yscrollcommand=scrollbar.set)

    # Создание заголовков столбцов таблицы
    tk.Label(details_container, text="Фамилия ученика", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=0, sticky="nsew")
    tk.Label(details_container, text="Имя ученика", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=1, sticky="nsew")
    tk.Label(details_container, text="Дата рождения ученика", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=2, sticky="nsew")
    tk.Label(details_container, text="Оценка", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=3, sticky="nsew")
    tk.Label(details_container, text="Замечания", bd=1, bg="#D9D9D9", relief=tk.SOLID).grid(row=0, column=4, sticky="nsew")

    # Заполнение таблицы данными
    view_lesson_details(lesson_id)

    # Создание кнопок для отмены и добавления новой оценки урока
    cancel_button = tk.Button(window, text="Отмена", command=window.destroy)
    cancel_button.place(x=100, y=450)
    add_lesson_button = tk.Button(window, text="Новая оценка", command=lambda: open_new_mark(lesson_id, window))
    add_lesson_button.place(x=600, y=450)


# Функция просмотра подробной информации о занятии
def view_lesson_details(lesson_id):
    # Создаем курсор для работы с базой данных
    cursor = connection.cursor()
    # Исполняем запрос на получение данных учеников и их оценок по данному занятию
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
    # Получаем все строки с данными из запроса
    rows = cursor.fetchall()
    # Перебираем полученные данные и создаем виджеты Label для их отображения
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            tk.Label(details_container, text=value, bd=1, bg='white', relief=tk.SOLID).grid(row=i+1, column=j, sticky="nsew")


# Функция создания окна для добавления новой оценки ученика на урок
def open_new_mark(lesson_id, window_open_lesson_details):
    # Создаем новое окно
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
    # Получаем результат запроса в ответе
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
    # Выполняем запрос на получение списка учеников из базы данных и получаем результат в ответе
    cursor.execute("SELECT txtPupilSurname, txtPupilName FROM tblPupil")
    pupils = cursor.fetchall()
    # Создаем список с именами и фамилиями учеников в формате "Фамилия Имя"
    pupils_list = [f"{surname} {name}" for surname, name in pupils]
    # Создаем переменную для выбора ученика
    pupil_var = tk.StringVar(new_mark_window)
    # Задаем по умолчанию первого ученика из списка
    pupil_var.set(pupils_list[0])
    # Создаем выпадающий список для выбора ученика
    tk.OptionMenu(new_mark_window, pupil_var, *pupils_list).place(x=150, y=180)

    tk.Label(new_mark_window, text="Оценка:", font=("Arial", 14)).place(x=10, y=220)
    # Создаем переменную для выбора оценки
    mark_var = tk.StringVar(new_mark_window)
    # Задаем по умолчанию оценку "5"
    mark_var.set("5")
    # Создаем выпадающий список для выбора оценки
    tk.OptionMenu(new_mark_window, mark_var, "5", "4", "3", "2").place(x=150, y=220)

    tk.Label(new_mark_window, text="Замечания:", font=("Arial", 14)).place(x=10, y=260)
    # Создаем поле для ввода замечаний
    comment_entry = tk.Entry(new_mark_window, font=("Arial", 14), width=50)
    comment_entry.place(x=150, y=260)

    # Кнопки "Отмена" и "Добавить урок"
    cancel_button = tk.Button(new_mark_window, text="Отмена", command=new_mark_window.destroy)
    cancel_button.place(x=220, y=500)
    # Создаем кнопку для добавления новой оценки
    add_lesson_button = tk.Button(new_mark_window, text="Добавить оценку", command=lambda: submit_mark(lesson_id, pupil_var, mark_var, comment_entry, new_mark_window, window_open_lesson_details))
    add_lesson_button.place(x=620, y=500)


# Функция для сохранения оценки ученика к уроку
def submit_mark(lesson_id, pupil_var, mark_var, comment_entry, new_mark_window, window_open_lesson_details):
    # Получаем значения из элементов интерфейса
    pupil_var = pupil_var.get() # Получаем данные ученика
    pupil_surname, pupil_name = pupil_var.split(" ") # Разделяем полученные данные по пробелу

    cursor = connection.cursor()
    # Выводим id ученика из таблицы tblPupil, используя его имя и фамилию
    cursor.execute(""" 
        SELECT intPupilId
        FROM tblPupil
        WHERE txtPupilName = ? AND txtPupilSurname = ? 
    """, (pupil_name, pupil_surname))
    pupil_id = cursor.fetchone()[0] # Присваиваем значение id ученика

    mark_value = mark_var.get() # Получаем значение оценки из элемента интерфейса
    mark_comment = comment_entry.get() # Получаем комментарий оценки из элемента интерфейса

    # Добавляем информацию об оценке в базу данных в таблицу tblMark
    cursor.execute("""
        INSERT INTO tblMark (intLessonId, intPupilId, intMarkValue, txtMarkComment)
        VALUES (?, ?, ?, ?)
    """, (lesson_id, pupil_id, mark_value, mark_comment))

    connection.commit() # Подтверждаем изменения в базе данных

    new_mark_window.destroy() # Закрываем окно добавления оценки
    window_open_lesson_details.destroy() # Закрываем окно задания урока
    open_lesson_details(lesson_id) # Открываем окно задания урока, обновив информацию о нём


# Создаем графическое окно
lessons = tk.Tk()
lessons.title("Уроки")
lessons.geometry("1000x710")
lessons.configure(bg="#F0F0F0")

# Выводим список уроков в таблице
view_lessons()

# Создаем кнопку для добавления нового урока
add_lesson_button = tk.Button(lessons, text="Добавить урок", command=add_lesson)
add_lesson_button.place(relx=0.5, y=670, anchor=tk.CENTER)
add_lesson_button.config(width=20, height=2)

# Запускаем главный цикл обработки событий графического интерфейса
lessons.mainloop()

