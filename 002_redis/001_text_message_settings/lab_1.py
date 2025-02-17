# Импорт необходимых модулей
import redis
from tkinter import *

# Подключение к Redis-серверу
client = redis.Redis(host='localhost', port=6379, db=0)

# Кнопка для сохранения настроек
def settings():
    # Получение данных из виджетов
    styleName = valueInside.get()
    text1 = txt5.get()
    font = valueF.get()
    font += ";"
    font += "{}".format(txt2.get())
    font += ";"
    fontColor = valueColor.get()
    font += valueFont.get()

    # Сохранение данных в Redis
    client.set(styleName, "{},{}".format(font, fontColor))

    # Чтение сохраненных данных из Redis и обновление отображения
    info = client.get(styleName).decode().split(",")
    info1 = info[0].split(";")
    txt15.config(text=text1, font=(info1[0], info1[1], info1[2]), fg=info[1])

# Кнопка для применения настроек
def apply(styleName):
    # Получение данных из виджетов
    styleName = valueInside.get()

    # Проверка существования стиля в Redis
    if client.exists(styleName):
        text1 = txt5.get()
        info = client.get(styleName).decode().split(",")
        info1 = info[0].split(";")

        # Обновление отображения с учетом сохраненных данных
        txt15.config(text=text1, font=(info1[0], info1[1], info1[2]), fg=info[1])

# Функция вызываемая при каждом нажатии клавиши в виджете ввода текста
def on_key_press(event):
    apply(valueInside.get())

# Создание главного окна
window = Tk()
window.geometry('900x700')
window.title("СУБД Redis")
window.resizable(width=True, height=True)

# Создание верхней и нижней рамок
f_top = Frame(window)
f_bot = Frame(window)

# Инициализация списка стилей
listOfStyles = ['style1', 'style2', 'style3']
valueInside = StringVar(f_top)
valueInside.set('style1')

# Создание виджетов для ввода имени стиля
lbl = Label(f_top, text="Выберете стиль", font=20)
txt = OptionMenu(f_top, valueInside, *listOfStyles, command=apply)

# Инициализация списка шрифтов
listOFF = ['Times New Roman', 'Calibri Light', 'STXingkai', 'Comic Sans MS', 'Arial Black']
valueF = StringVar(f_top)
valueF.set('Times New Roman')

# Создание виджетов для выбора шрифта
lbl1 = Label(f_top, text="Выберите название шрифта", font=20)
txt1 = OptionMenu(f_top, valueF, *listOFF)

# Создание виджетов для ввода размера шрифта
lbl2 = Label(f_top, text="Введите размер шрифта", font=20)
txt2 = Entry(f_top, width=90)

# Инициализация списка цветов
listOfColors = ['black', 'red', 'blue', 'green', 'yellow']
valueColor = StringVar(f_top)
valueColor.set('black')

# Создание виджетов для выбора цвета шрифта
lbl3 = Label(f_top, text="Выберите цвет шрифта", font=20)
txt3 = OptionMenu(f_top, valueColor, *listOfColors)

# Инициализация списка начертаний шрифта
listOfFonts = ['normal', 'bold', 'italic', 'overstrike']
valueFont = StringVar(f_top)
valueFont.set('normal')

# Создание виджетов для выбора начертания шрифта
lbl4 = Label(f_top, text="Выберите начертание шрифта", font=20)
txt4 = OptionMenu(f_top, valueFont, *listOfFonts)

# Создание виджетов для ввода текста
lbl5 = Label(f_top, text="Введите текст", font=20)
txt5 = Entry(f_top, width=90)

# Виджет для отображения текста с примененными настройками
txt15 = Label(f_top, text='')

# Кнопка для сохранения настроек
btn = Button(f_top, text="Сохранить", command=settings)

# Привязка функции on_key_press к событию <Key> виджета ввода текста
txt5.bind('<KeyRelease>', on_key_press)

# Размещение виджетов на главном окне
f_top.pack(side=LEFT, ipadx=10, ipady=100)
lbl.pack(side=TOP)
txt.pack(side=TOP)
lbl1.pack(side=TOP)
txt1.pack(side=TOP)
lbl2.pack(side=TOP)
txt2.pack(side=TOP)
lbl3.pack(side=TOP)
txt3.pack(side=TOP)
lbl4.pack(side=TOP)
txt4.pack(side=TOP)
lbl5.pack(side=TOP)
txt5.pack(side=TOP)
txt15.pack(side=TOP)
btn.pack(side=LEFT, padx=20)

# Запуск главного цикла обработки событий
window.mainloop()
