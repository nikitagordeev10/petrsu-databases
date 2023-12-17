# Импортируем необходимые модули
import tkinter as tk
import pyodbc

# Подключение к базе данных SQL Server
connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10', database='master', user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')

# Функция для просмотра списка уроков
def view_lessons():
    # Создаем холст с полосой прокрутки
    canvas = tk.Canvas(lessons, bg='white')
    canvas.place(x=10, y=20, relwidth=0.96, height=620)
    scrollbar = tk.Scrollbar(lessons, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.place(relx=0.96, y=20, height=620)

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

    # Добавляем необходимое количество строк с пустыми ячейками
    for i in range(1, num_rows+1):
        tk.Label(table_container, text="", bg="white", bd=1, relief=tk.SOLID).grid(row=i, column=0, sticky="nsew")
        tk.Label(table_container, text="", bg="white", bd=1, relief=tk.SOLID).grid(row=i, column=1, sticky="nsew")
        tk.Label(table_container, text="", bg="white", bd=1, relief=tk.SOLID).grid(row=i, column=2, sticky="nsew")
        tk.Label(table_container, text="", bg="white", bd=1, relief=tk.SOLID).grid(row=i, column=3, sticky="nsew")
    
    # Создаем объект курсора для выполнения SQL запросов
    cursor = connection.cursor()
    # Выполняем запрос на выборку данных из трех таблиц базы данных
    cursor.execute("""
            SELECT 
                tblSubject.txtSubjectName, 
                tblLesson.datLessonDate, 
                tblLesson.txtTheme, 
                tblTeacher.txtTeacherName
            FROM 
                tblSubject, tblTeacher, tblLesson
            WHERE 
                (tblSubject.intSubjectId = tblLesson.intSubjectId) and (tblSubject.intTeacherId = tblTeacher.intTeacherId)
    """)
    rows = cursor.fetchall()
    # Отображаем полученную информацию в таблице
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            tk.Label(table_container, text=value, bd=1, bg='white', relief=tk.SOLID).grid(row=i+1, column=j, sticky="nsew")

# Функция добавления нового урока
def add_lesson():
    pass

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

