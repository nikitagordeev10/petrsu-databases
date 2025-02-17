# Импортируем необходимые библиотеки
import tkinter as tk
import pyodbc

# Устанавливаем соединение с базой данных
connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10', database='master',
                            user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')

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

# Создаем главное окно приложения для отображения списка уроков и кнопки добавления нового урока
lessons = tk.Tk()
lessons.title("Уроки")
lessons.geometry("1000x710")
lessons.configure(bg="#F0F0F0")

add_lesson_button = tk.Button(lessons, text="Добавить урок", command=add_lesson)
add_lesson_button.place(relx=0.5, y=670, anchor=tk.CENTER)
add_lesson_button.config(width=20, height=2)

lessons.mainloop()

