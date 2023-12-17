import pymongo
from tkinter import *
from tkinter import ttk
import json

# Подключение к MongoDB
client = pymongo.MongoClient('localhost')
database = client['22307']

# Создание коллекции
football_collection = database["football_data"]
game_collection = database["game_data"]
collections_names = ['Футбольные команды', 'Игры']

"""
Оконное приложение для поиска и отображения результатов
"""
class Task3:
    def __init__(self, master):
        # Инициализация приложения
        self.master = master
        self.master.title("task_3")

        # Настройка интерфейса
        self.setup_ui()

        # Установка начальной коллекции
        self.current_collection = football_collection

    def setup_ui(self):
        # Настройка шрифта и стиля
        font_style = ("Helvetica", 12)
        title_font_style = ("Helvetica", 16, "bold")

        # Добавленный заголовок
        title_label = Label(self.master, text="Поиск и вывод результатов", font=title_font_style)
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Коллекция
        Label(self.master, text="Коллекция:", font=font_style).grid(row=1, column=0)
        self.collection_var = StringVar()
        self.collection_entry = ttk.Combobox(self.master, textvariable=self.collection_var, values=collections_names, font=font_style)
        self.collection_entry.grid(row=1, column=1, columnspan=1)
        self.collection_entry.bind("<<ComboboxSelected>>", lambda event: self.choose_current_collection())

        # Ключ
        Label(self.master, text="Ключ:", font=font_style).grid(row=2, column=0)
        self.key_var = StringVar()
        self.key_entry = ttk.Combobox(self.master, textvariable=self.key_var, font=font_style)
        self.key_entry.grid(row=2, column=1)

        # Сравнение
        Label(self.master, text="Сравнение:", font=font_style).grid(row=3, column=0)
        self.comparison_var = StringVar()
        self.comparison_entry = ttk.Combobox(self.master, textvariable=self.comparison_var, values=['>', '>=', '=', '<=', '<', '!='], font=font_style)
        self.comparison_entry.grid(row=3, column=1)

        # Значение
        Label(self.master, text="Значение:", font=font_style).grid(row=4, column=0)
        self.value_entry = Entry(self.master, font=font_style)
        self.value_entry.grid(row=4, column=1)

        # Кнопка поиска
        self.search_button = Button(self.master, text="Выполнить запрос", command=self.perform_search, font=font_style)
        self.search_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Текущая коллекция
        Label(self.master, text="Текущая коллекция:", font=font_style).grid(row=6, column=0)
        self.current_collection_label2 = Label(self.master, text="Футбольные команды", font=font_style)
        self.current_collection_label2.grid(row=6, column=1)

        # Текстовое поле для отображения документов
        self.documents_text = Text(self.master, width=75, height=15, state="disabled", font=font_style)
        self.documents_text.grid(row=7, column=0, columnspan=2, padx=40, pady=10)

    def choose_current_collection(self):
        # Выбор текущей коллекции при смене значения в выпадающем списке
        cur_collection = self.collection_var.get()
        if cur_collection == collections_names[1]:
            self.current_collection = game_collection
            self.current_collection_label2.config(text=collections_names[1])
            self.key_entry['values'] = self.game_keys
        else:
            self.current_collection = football_collection
            self.current_collection_label2.config(text=collections_names[0])
            self.key_entry['values'] = self.football_keys

    def show_documents(self, query):
        # Отображение документов в текстовом поле
        self.documents_text.config(state=NORMAL)
        self.documents_text.delete(1.0, END)

        for document in self.current_collection.find(query):
            separator_line = "\n" + "_" * 40 + "\n\n"
            self.documents_text.insert(END, json.dumps({x: document[x] for x in document if x not in "_id"}, indent=4, ensure_ascii=False) + separator_line)

        self.documents_text.config(state="disabled")

    def perform_search(self):
        # Выполнение поиска по введенным критериям
        key = self.key_var.get()
        comparison = self.comparison_var.get()
        value = self.value_entry.get()

        # Преобразование значения в соответствующий тип (int, float, str)
        try:
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            pass  # Если не удалось преобразовать в число, оставляем как строку

        # Определение оператора сравнения
        if comparison == '>':
            query = {key: {'$gt': value}}
        elif comparison == '>=':
            query = {key: {'$gte': value}}
        elif comparison == '=':
            query = {key: {'$eq': value}}
        elif comparison == '<=':
            query = {key: {'$lte': value}}
        elif comparison == '<':
            query = {key: {'$lt': value}}
        elif comparison == '!=':
            query = {key: {'$ne': value}}
        else:
            # Обработка некорректного сравнения
            print("Некорректное сравнение")

        # Выполнение запроса к коллекции
        self.show_documents(query)

# Запуск оконных приложений
root2 = Tk()
root2.geometry('800x600')

# Ключи для каждой коллекции
search_app = Task3(root2)
search_app.football_keys = [
            "дата", "счёт", "запасные игроки.0.ФИО", "запасные игроки.0.позиция",
            "состав игроков.0.ФИО", "состав игроков.0.позиция", "состав игроков.1.ФИО", "состав игроков.1.позиция",
            "ФИО тренера", "город", "название"
        ]

search_app.game_keys = [
    "дата", "счёт", "забитые мячи.0.положение", "забитые мячи.0.минута", "забитые мячи.0.автор", "забитые мячи.0.передачи",
    "забитые мячи.1.положение", "забитые мячи.1.минута", "забитые мячи.1.автор", "забитые мячи.1.передачи",
    "забитые мячи.2.положение", "забитые мячи.2.минута", "забитые мячи.2.автор", "забитые мячи.2.передачи",
    "количество ударов по воротам.0.положение", "количество ударов по воротам.0.минута", "количество ударов по воротам.0.автор",
    "количество ударов по воротам.0.передачи", "пенальти.0.положение", "пенальти.0.минута", "пенальти.0.автор",
    "пенальти.0.передачи", "нарушения правил.0.жёлтые карточки", "нарушения правил.0.красные карточки",
    "нарушения правил.0.кому", "нарушения правил.0.минута", "нарушения правил.0.причина"
]

root2.mainloop()
