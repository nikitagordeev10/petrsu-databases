import tkinter as tk
from tkinter import messagebox
from lab_10 import create_report_lab_10
from lab_11 import create_report_lab_11
from lab_12 import create_report_lab_12
import os
import pyodbc
import subprocess

# Функция для получения списка предметов из базы данных
def get_subjects():
    subjects = []
    connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10', database='master', user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')
    cursor = connection.cursor()
    for row in cursor.execute("SELECT txtSubjectName FROM tblSubject"):
        subjects.append(row.txtSubjectName)
    connection.close()
    return subjects

# Функция, которая запускает программу
def run_lessons():
    os.chdir(os.getcwd()) # переходим в директорию с файлом lessons.py
    subprocess.Popen(["python", "lab_6_7_8_9.py"]) # запускаем файл lessons.py в новом процессе

def generate_report_lab_10():
    try:
        create_report_lab_10()
        messagebox.showinfo(title="Отчет", message="Отчет сгенерирован успешно!")
    except:
        messagebox.showerror(title="Ошибка", message="Произошла ошибка при генерации отчета.")

def generate_report_lab_11():
    try:
        create_report_lab_11()
        messagebox.showinfo(title="Отчет", message="Отчет сгенерирован успешно!")
    except:
        messagebox.showerror(title="Ошибка", message="Произошла ошибка при генерации отчета.")

def generate_report_lab_12():
    # функция-обработчик события нажатия кнопки
    subject_name = subject_var.get() 
    if not subject_name:
        messagebox.showerror(title="Ошибка", message="Введите название предмета!")
        return
    try:
        create_report_lab_12(subject_name)
        messagebox.showinfo(title="Отчет", message="Отчет сгенерирован успешно!")
    except:
        messagebox.showerror(title="Ошибка", message="Произошла ошибка при генерации отчета.")


# Создание окна с полем для ввода названия предмета и кнопкой
root = tk.Tk()
root.title("Школьный журнал")
root.geometry("900x600")
root.configure(bg="#D9D9D9")

# Разделяем окно на две части через главный фрейм
main_frame = tk.Frame(root, bg="#D9D9D9")
main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Создаем левую часть окна
left_frame = tk.Frame(main_frame, bg="#D9D9D9")
left_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

# Создаем заголовок для левой части
journal_title_label = tk.Label(left_frame, text="Школьный журнал", font=("Helvetica", 24), bg="#D9D9D9")
journal_title_label.pack(side=tk.TOP, padx=10, pady=10)

# Создаем кнопку открытия уроков
open_lessons_button = tk.Button(left_frame, text="Открыть уроки", font=("Helvetica", 24), command=run_lessons, bg="#C2C2C2", bd=1, relief=tk.SOLID, width=17, height=10)
open_lessons_button.pack(side=tk.TOP, padx=10, pady=10, expand=True)

# Добавляем вертикальную черную черту для отделения правой и левой сторон
separator = tk.Frame(main_frame, width=2, bg="black")
separator.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

# Создаем правую часть окна
right_frame = tk.Frame(main_frame, bg="#D9D9D9")
right_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

# Создаем заголовок для верхней части правой части
reports_title_label = tk.Label(right_frame, text="Отчеты", font=("Helvetica", 24), bg="#D9D9D9")
reports_title_label.pack(side=tk.TOP, padx=10, pady=10)

# Создаем кнопку учителей
teachers_button = tk.Button(right_frame, text="Учителя", font=("Helvetica", 24), command=generate_report_lab_10, bg="#C2C2C2", bd=1, relief=tk.SOLID, width=17)
teachers_button.pack(side=tk.TOP, padx=10, pady=10, expand=True)

# Создаем кнопку для ведомости
register_button = tk.Button(right_frame, text="Ведомость", font=("Helvetica", 24), command=generate_report_lab_11, bg="#C2C2C2", bd=1, relief=tk.SOLID, width=17)
register_button.pack(side=tk.TOP, padx=10, pady=10, expand=True)

# Создаем кнопку "Школьный журнал"
journal_button = tk.Button(right_frame, text="Школьный журнал", font=("Helvetica", 24), command=generate_report_lab_12, bg="#C2C2C2", bd=1, relief=tk.SOLID, width=17)
journal_button.pack(side=tk.TOP, padx=10, pady=10, expand=True)

# Создаем поле для ввода названия предмета
subject_name_label = tk.Label(right_frame, text="Введите предмет:", font=("Helvetica", 14), bg="#D9D9D9")
subject_name_label.pack(side=tk.TOP, padx=10, pady=10)

subjects = get_subjects()  # Получение списка предметов из базы данных
subject_var = tk.StringVar(right_frame)
subject_var.set(subjects[0]) 

subject_menu = tk.OptionMenu(right_frame, subject_var, *subjects)
subject_menu.config(width=20, font=("Helvetica", 14))
subject_menu.pack(pady=10)

# Запускаем главный цикл обработки событий графического интерфейса
root.mainloop()