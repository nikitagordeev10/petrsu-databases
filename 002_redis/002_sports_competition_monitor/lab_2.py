import tkinter as tk
from tkinter import ttk
import redis

# Создание соединения с Redis
connection = redis.Redis(host='localhost', port=6379, db=0)
def save_score():
    # Получаем выбранных спортсменов, судью и введенные баллы
    selected_sportsman = sportsman_var.get()
    selected_judge = judge_var.get()
    entered_score = int(score_entry.get())

    # Проверяем, что введенные баллы неотрицательные
    if entered_score >= 0:
        # Создаем ключ для хранения оценки
        score_key = f"sportsman:{selected_sportsman}:{selected_judge}"

        # Проверяем, не выставлял ли судья баллы ранее
        if not connection.exists(score_key):
            # Увеличиваем счетчик баллов и обновляем рейтинг
            connection.hincrby(score_key, "score", entered_score)
            update_rankings()

def update_rankings():
    # Очищаем список рейтинга
    rankings_listbox.delete(0, tk.END)

    # Получаем и сортируем рейтинги и добавляем их в список
    for sportsman, score in get_rankings():
        rankings_listbox.insert(tk.END, f'{sportsman}: {score}')


def get_rankings():
    # Получаем имена всех спортсменов из базы данных
    sportsman_keys = connection.keys('sportsman:*')
    sportsmans = set(key.decode().split(':')[1] for key in sportsman_keys)

    # Вычисляем общий балл для каждого спортсмена
    rankings = {}
    for sportsman in sportsmans:
        sportsman_score_keys = connection.keys(f"sportsman:{sportsman}:*")
        # Предположим, что sportsman_score_keys уже определено

        # Инициализируем переменную для суммы
        score_sum = 0

        # Цикл for наружу
        for key in sportsman_score_keys:
            # Добавляем к сумме значение из хранилища
            score_sum += int(connection.hget(key, "score"))

        # Теперь переменная score_sum содержит общую сумму
        rankings[sportsman] = score_sum

    # Сортируем рейтинг по убыванию
    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)

    return sorted_rankings

def clear_rankings():
    # Очищаем рейтинги для всех спортсменов и судей
    for sportsman in sportsman_names:
        for judge in judge_names:
            connection.delete(f"sportsman:{sportsman}:{judge}")

# Создаем основное окно
root = tk.Tk()
root.title("Sportivnyy monitor")
root.geometry('500x500')

# Настраиваем стили элементов интерфейса
style = ttk.Style()
style.configure('TLabel', font=('Arial', 12), anchor='w')
style.configure('TCombobox', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))
style.configure('TListbox', font=('Arial', 12), anchor='w')

# Определяем имена спортсменов и судей
sportsman_names = ["Sportsmen 1", "Sportsmen 2", "Sportsmen 3", "Sportsmen 4", "Sportsmen 5"]
judge_names = ["Sudya 1", "Sudya 2", "Sudya 3", "Sudya 4", "Sudya 5"]

# Создаем и настраиваем виджеты интерфейса
judge_label = ttk.Label(root, text="Sudya:")
judge_var = tk.StringVar()
judge_combobox = ttk.Combobox(root, textvariable=judge_var, values=judge_names, style='TCombobox')
score_label = ttk.Label(root, text="Bally:")
score_entry = ttk.Entry(root, style='TEntry')
sportsman_label = ttk.Label(root, text="Sportsmen:")
sportsman_var = tk.StringVar()
sportsman_combobox = ttk.Combobox(root, textvariable=sportsman_var, values=sportsman_names, style='TCombobox')
save_button = ttk.Button(root, text="Sokhranit Bally", command=save_score, style='TButton')
rankings_label = ttk.Label(root, text="Reyting Sportsmenов:")
rankings_listbox = tk.Listbox(root, font=('Arial', 12), selectbackground='#a6a6a6', selectforeground='white')

# Размещаем виджеты на форме
judge_label.grid(row=0, column=0, pady=5, sticky='w')
judge_combobox.grid(row=0, column=1, pady=5)
score_label.grid(row=1, column=0, pady=5, sticky='w')
score_entry.grid(row=1, column=1, pady=5, padx=5)
sportsman_label.grid(row=2, column=0, pady=5, sticky='w')
sportsman_combobox.grid(row=2, column=1, pady=5)
save_button.grid(row=3, column=0, pady=10, padx=5, columnspan=2, sticky='w')
rankings_label.grid(row=4, column=0, columnspan=2, pady=5, sticky='w')
rankings_listbox.grid(row=5, column=0, columnspan=2, pady=5, sticky='w')

# Очищаем рейтинги при запуске
clear_rankings()

# Создаём таблицу
for name in sportsman_names:
    score_key = f"sportsman:{name}:default"
    connection.hincrby(score_key, "score", 0)
    update_rankings()

# Запускаем главный цикл событий
root.mainloop()