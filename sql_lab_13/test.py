import tkinter as tk
from tkinter import messagebox
from lab_12 import create_report_lab_12
import pyodbc

# Функция для получения списка предметов из базы данных
def get_subjects():
    subjects = []
    connection = pyodbc.connect(driver='{SQL Server}', server='NIKITAGORDEEV10', database='master', user='NIKITAGORDEEV10\nikit', Trusted_Connection='yes')
    cursor = connection.cursor()
    for row in cursor.execute("SELECT txtSubjectName FROM tblSubject"):
        subjects.append(row.txtSubjectName)
    connection.close()
    return subjects


def generate_report_lab_12():
    subject_name = subject_var.get() 
    if not subject_name:
        messagebox.showerror(title="Ошибка", message="Выберите предмет!")
        return
    try:
        create_report_lab_12(subject_name)
        messagebox.showinfo(title="Отчет", message="Отчет сгенерирован успешно!")
    except:
        messagebox.showerror(title="Ошибка", message="Произошла ошибка при генерации отчета.")


root = tk.Tk()
root.title("Школьный журнал")
root.geometry("900x600")

subjects = get_subjects()  # Получение списка предметов из базы данных

subject_var = tk.StringVar(root)
subject_var.set(subjects[0]) 

subject_menu = tk.OptionMenu(root, subject_var, *subjects)
subject_menu.config(width=20, font=("Helvetica", 14))
subject_menu.pack(pady=20)

# journal_button = tk.Button(root, text="Школьный журнал", font=("Helvetica", 24), command=generate_report_lab_12, bg="#C2C2C2", bd=1, relief=tk.SOLID, width=17)
# journal_button.pack(side=tk.TOP, padx=10, pady=10, expand=True)

root.mainloop()
