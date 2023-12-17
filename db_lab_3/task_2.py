import pymongo
from tkinter import *
from tkinter import ttk
import json

# Подключение к MongoDB
def connect_to_mongo():
    # Создание клиента MongoDB и подключение к базе данных
    client = pymongo.MongoClient('localhost')
    database = client['22307']

    # Получение коллекций
    football_collection = database["football_data"]
    game_collection = database["game_data"]
    collections_names = ['Футбольные команды', 'Игры']
    return football_collection, game_collection, collections_names

class Task2:
    # Инициализация приложения
    def __init__(self, master, football_collection, game_collection, collections_names):
        self.master = master
        self.master.title("task_2")
        self.football_collection = football_collection
        self.game_collection = game_collection
        self.collections_names = collections_names
        self.current_document = {}
        self.current_collection = self.football_collection

        # Словари ключей для каждой коллекции
        self.football_keys = [
            "дата", "счёт", "запасные игроки.0.ФИО", "запасные игроки.0.позиция",
            "состав игроков.0.ФИО", "состав игроков.0.позиция", "состав игроков.1.ФИО", "состав игроков.1.позиция",
            "ФИО тренера", "город", "название"
        ]

        self.game_keys = [
            "дата", "счёт", "забитые мячи.0.положение", "забитые мячи.0.минута", "забитые мячи.0.автор", "забитые мячи.0.передачи",
            "забитые мячи.1.положение", "забитые мячи.1.минута", "забитые мячи.1.автор", "забитые мячи.1.передачи",
            "забитые мячи.2.положение", "забитые мячи.2.минута", "забитые мячи.2.автор", "забитые мячи.2.передачи",
            "количество ударов по воротам.0.положение", "количество ударов по воротам.0.минута", "количество ударов по воротам.0.автор",
            "количество ударов по воротам.0.передачи", "пенальти.0.положение", "пенальти.0.минута", "пенальти.0.автор",
            "пенальти.0.передачи", "нарушения правил.0.жёлтые карточки", "нарушения правил.0.красные карточки",
            "нарушения правил.0.кому", "нарушения правил.0.минута", "нарушения правил.0.причина"
        ]

        # Настройка пользовательского интерфейса
        self.setup_ui()

    def setup_ui(self):
        # Настройка шрифта и стиля
        font_style = ("Helvetica", 12)
        title_font_style = ("Helvetica", 16, "bold")

        # Заголовок
        title_label = Label(self.master, text="Ввод и отображение информации", font=title_font_style)
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Коллекция
        Label(self.master, text="Коллекция:", font=font_style).grid(row=1, column=0)
        self.collection_var = StringVar()
        self.collection_entry = ttk.Combobox(self.master, textvariable=self.collection_var,
                                             values=self.collections_names, font=font_style)
        self.collection_entry.grid(row=1, column=1)
        self.collection_entry.bind("<<ComboboxSelected>>", lambda event: self.choose_current_collection())

        # Ключ (выпадающий список)
        Label(self.master, text="Ключ:", font=font_style).grid(row=2, column=0)
        self.key_combobox = ttk.Combobox(self.master, font=font_style)
        self.key_combobox.grid(row=2, column=1)

        # Значение
        Label(self.master, text="Значение:", font=font_style).grid(row=3, column=0)
        self.value_entry = Entry(self.master, font=font_style)
        self.value_entry.grid(row=3, column=1)

        # Кнопки
        Button(self.master, text="Добавить ключ-значение", command=self.add_key_value, font=font_style).grid(row=4,
                                                                                                             column=0,
                                                                                                             columnspan=3,
                                                                                                             pady=10)
        Button(self.master, text="Сохранить документ", command=self.save_document, font=font_style).grid(row=5,
                                                                                                         column=0,
                                                                                                         columnspan=3,
                                                                                                         pady=10)
        Button(self.master, text="Показать документы", command=self.show_documents, font=font_style).grid(row=6,
                                                                                                          column=0,
                                                                                                          columnspan=3,
                                                                                                          pady=10)

        # Текущая коллекция
        Label(self.master, text="Текущая коллекция:", font=font_style).grid(row=7, column=0)
        self.current_collection_label = Label(self.master, text="Футбольные команды", font=font_style)
        self.current_collection_label.grid(row=7, column=1)

        # Текстовое поле для документов
        self.documents_text = Text(self.master, width=70, height=20, state="disabled", font=font_style)
        self.documents_text.grid(row=8, column=0, columnspan=3, padx=40, pady=10)

    def view_current_document(self):
        # Отображение текущего документа в текстовом поле
        self.documents_text.config(state=NORMAL)
        self.documents_text.delete(1.0, END)
        separator_line = "\n" + "_" * 40 + "\n\n"
        self.documents_text.insert(END, json.dumps(
            {x: self.current_document[x] for x in self.current_document if x != "_id"}, indent=4,
            ensure_ascii=False) + separator_line)
        self.documents_text.config(state="disabled")

    def choose_current_collection(self):
        # Выбор текущей коллекции при смене значения в выпадающем списке
        cur_collection = self.collection_var.get()
        self.current_collection = self.game_collection if cur_collection == self.collections_names[
            1] else self.football_collection
        self.current_collection_label.config(text=cur_collection)

        # Установка ключей в выпадающем списке
        if cur_collection == 'Футбольные команды':
            self.key_combobox['values'] = self.football_keys
        elif cur_collection == 'Игры':
            self.key_combobox['values'] = self.game_keys

    def add_key_value(self):
        # Добавление ключ-значение в текущий документ
        key = self.key_combobox.get()
        value = self.value_entry.get()

        try:
            value = int(value)
        except ValueError:
            pass

        keys = key.split('.')
        self.update_document(keys, value)

    def update_document(self, keys, value):
        # Обновление текущего документа
        current_dict = self.current_document
        for i, key_part in enumerate(keys):
            if i == len(keys) - 1:
                current_dict[key_part] = value
            else:
                current_dict = current_dict.setdefault(key_part, {})

        self.view_current_document()

    def save_document(self):
        # Сохранение текущего документа в базе данных
        if self.current_document:
            self.current_collection.insert_one(self.current_document)
            self.current_document = {}

    def show_documents(self):
        # Отображение всех документов текущей коллекции
        self.documents_text.config(state=NORMAL)
        self.documents_text.delete(1.0, END)

        for document in self.current_collection.find():
            separator_line = "\n" + "_" * 40 + "\n\n"
            self.documents_text.insert(END, json.dumps({x: document[x] for x in document if x != "_id"}, indent=4,
                                                       ensure_ascii=False) + separator_line)

        self.documents_text.config(state="disabled")

# Подключение к MongoDB
football_collection, game_collection, collections_names = connect_to_mongo()

# Запуск оконного приложения
root1 = Tk()
root1.geometry('800x700')
football_app = Task2(root1, football_collection, game_collection, collections_names)
root1.mainloop()
