import pymongo
import tkinter as tk
from tkinter import ttk
import json

SEPARATOR = "_______________________________________\n\n"

# Подключение
client = pymongo.MongoClient('localhost')
database = client['22307']
# Создание коллекции
collection = database["online_store"]


class ProductQueryApp:
    listCategory = sorted(list(collection.distinct("category")))
    listCustomer = sorted(list(collection.distinct("customers.name")))
    listColors = sorted(list(collection.distinct("characteristics.color")))
    listProducts = sorted(list(collection.distinct("category")))
    listDeliveries = sorted(list(collection.distinct("customers.method_obtaining")))

    def __init__(self, master, collection):
        self.master = master
        self.master.title("Запросы к базе данных интернет-магазина")

        self.collection = collection

        # Стили для кнопок и меток
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#000", foreground="#000")
        style.configure("TLabel", padding=6, background="#eee")

        # Заголовок
        self.category_label0 = ttk.Label(self.master, text="Запросы к базе данных интернет-магазина:",
                                         font=('Arial', 14, 'bold'))
        self.category_label0.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

        # Вертикальная черта
        ttk.Separator(self.master, orient="horizontal").grid(row=1, column=0, columnspan=5, sticky="ew", pady=5)


        # Первый запрос
        self.category_label1 = ttk.Label(self.master, text="Список названий товаров, относящихся к заданной категории:")
        self.category_label1.grid(row=2, column=0, padx=10, pady=5)

        self.collection_var1 = tk.StringVar()
        self.collection_entry1 = ttk.Combobox(master, textvariable=self.collection_var1, values=self.listCategory)
        self.collection_entry1.grid(row=3, column=0)

        self.query_button_1 = ttk.Button(self.master, text="Показать",
                                         command=self.list_product_names_belong_given_category)
        self.query_button_1.grid(row=4, column=0, padx=10, pady=5)

        # Вертикальная черта
        ttk.Separator(self.master, orient="vertical").grid(row=2, column=1, rowspan=3, sticky="ns", padx=10)

        # Второй запрос
        self.category_label2 = ttk.Label(self.master, text="Характеристики товаров заданной категории:")
        self.category_label2.grid(row=2, column=2, padx=10, pady=5)

        self.collection_var2 = tk.StringVar()
        self.collection_entry2 = ttk.Combobox(master, textvariable=self.collection_var2, values=self.listCategory)
        self.collection_entry2.grid(row=3, column=2)

        self.query_button_2 = ttk.Button(self.master, text="Показать",
                                         command=self.list_characteristics_goods_given_category)
        self.query_button_2.grid(row=4, column=2, padx=10, pady=5)

        # Вертикальная черта
        ttk.Separator(self.master, orient="vertical").grid(row=2, column=3, rowspan=3, sticky="ns", padx=10)

        # Третий запрос
        self.category_label3 = ttk.Label(self.master, text="Названия и стоимость товаров, купленных заданным покупателем:")
        self.category_label3.grid(row=2, column=4, padx=10, pady=5)

        self.collection_var3 = tk.StringVar()
        self.collection_entry3 = ttk.Combobox(master, textvariable=self.collection_var3, values=self.listCustomer)
        self.collection_entry3.grid(row=3, column=4)

        self.query_button_3 = ttk.Button(self.master, text="Показать",
                                         command=self.get_products_by_customer)
        self.query_button_3.grid(row=4, column=4, padx=10, pady=5)

        # Горизонтальная черта
        ttk.Separator(self.master, orient="horizontal").grid(row=5, column=0, columnspan=5, sticky="ew", pady=5)

        # Четвертый запрос
        self.category_label4 = ttk.Label(self.master, text="Названия, производители и цены на товары, имеющие заданный цвет:")
        self.category_label4.grid(row=6, column=0, padx=10, pady=5)

        self.collection_var4 = tk.StringVar()
        self.collection_entry4 = ttk.Combobox(master, textvariable=self.collection_var4, values=self.listColors)
        self.collection_entry4.grid(row=7, column=0)

        self.query_button_4 = ttk.Button(self.master, text="Показать",
                                         command=self.get_products_by_color)
        self.query_button_4.grid(row=8, column=0, padx=10, pady=5)

        # Вертикальная черта
        ttk.Separator(self.master, orient="vertical").grid(row=6, column=1, rowspan=3, sticky="ns", padx=10)

        # Пятый запрос
        self.category_label5 = ttk.Label(self.master, text="Общая сумма проданных товаров:")
        self.category_label5.grid(row=6, column=2, padx=10, pady=5)

        self.query_button_5 = ttk.Button(self.master, text="Показать",
                                         command=self.get_total_sold_amount)
        self.query_button_5.grid(row=7, column=2, padx=10, pady=5)

        # Вертикальная черта
        ttk.Separator(self.master, orient="vertical").grid(row=6, column=3, rowspan=3, sticky="ns", padx=10)

        # Шестой запрос
        self.category_label6 = ttk.Label(self.master, text="Количество товаров в каждой категории:")
        self.category_label6.grid(row=6, column=4, padx=10, pady=5)

        self.query_button_6 = ttk.Button(self.master, text="Показать",
                                         command=self.get_products_count_by_category)
        self.query_button_6.grid(row=7, column=4, padx=10, pady=5)

        # Горизонтальная черта
        ttk.Separator(self.master, orient="horizontal").grid(row=9, column=0, columnspan=5, sticky="ew", pady=5)

        # Седьмой запрос
        self.category_label7 = ttk.Label(self.master, text="Список имен покупателей заданного товара:")
        self.category_label7.grid(row=10, column=0, padx=10, pady=5)

        self.collection_var7 = tk.StringVar()
        self.collection_entry7 = ttk.Combobox(master, textvariable=self.collection_var7, values=self.listProducts)
        self.collection_entry7.grid(row=11, column=0)

        self.query_button_7 = ttk.Button(self.master, text="Показать",
                                         command=self.get_customer_names_by_product)
        self.query_button_7.grid(row=12, column=0, padx=10, pady=5)

        # Вертикальная черта
        ttk.Separator(self.master, orient="vertical").grid(row=10, column=1, rowspan=3, sticky="ns", padx=10)

        # Восьмой запрос
        self.category_label8 = ttk.Label(self.master, text="Список имен покупателей заданного товара, с доставкой фирмы с заданным названием:")
        self.category_label8.grid(row=10, column=2, columnspan=3, padx=10, pady=5)

        self.collection_var8 = tk.StringVar()
        self.collection_entry8 = ttk.Combobox(master, textvariable=self.collection_var8, values=self.listProducts)
        self.collection_entry8.grid(row=11, column=2)


        self.collection_var8_1 = tk.StringVar()
        self.collection_entry8_1 = ttk.Combobox(master, textvariable=self.collection_var8_1, values=self.listDeliveries)
        self.collection_entry8_1.grid(row=11, column=4)

        self.query_button_8 = ttk.Button(self.master, text="Показать",
                                         command=self.get_customer_names_by_product_and_delivery)
        self.query_button_8.grid(row=12, column=2, columnspan=3, padx=10, pady=5)

        # Вертикальная черта
        ttk.Separator(self.master, orient="horizontal").grid(row=13, column=0, columnspan=5, sticky="ew", pady=5)

        # Блок с результатом
        self.result_label = ttk.Label(self.master, text="Результат:")
        self.result_label.grid(row=14, column=0, columnspan=2, padx=10, pady=5)

        self.result_text = tk.Text(self.master, height=10, width=70, state="disabled")
        self.result_text.grid(row=14, column=1, columnspan=3, padx=10, pady=5)


    #####################################################
    # 1 запрос
    def list_product_names_belong_given_category(self):
        category = self.collection_var1.get()
        result_text = ""

        pipeline = [
            {
                "$match": {"category": category}
            },
            {
            "$project": {
                "_id": 0,
                "category": 1,
                "manufacturer": 1,
                "model": 1
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline,
        )

        for item in a:
            result_text += f"Производитель: {item.get('manufacturer', 'N/A')}\nМодель: {item.get('model', 'N/A')}\n{SEPARATOR}"

        self.update_result_text(result_text)


    # 2 запрос
    def list_characteristics_goods_given_category(self):
        category = self.collection_var2.get()
        result_text = ""

        pipeline = [
            {
                "$match": {"category": category}
            },
            {
                "$project": {
                    "_id": 0,
                    "category": 1,
                    "characteristics": 1
                }
            }
        ]

        a = self.collection.aggregate(pipeline)
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)

        for doc in a:
            characteristics = doc.get('characteristics', {})

            if characteristics:  # Проверяем, есть ли характеристики
                result_text += "Характеристики:\n"

                for key, value in characteristics.items():
                    result_text += f"• {key}: {value}\n"
            else:
                result_text += "У товара нет характеристик\n"

            result_text += SEPARATOR

        self.result_text.insert(tk.END, result_text)
        self.result_text.config(state="disabled")

    # 3 запрос
    def get_products_by_customer(self):
        customer = self.collection_var3.get()
        result_text = ""

        pipeline = [
            {
                "$match": {"customers.name": customer}
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$category",
                    "manufacturer": "$manufacturer",
                    "model": "$model",
                    "price": "$price",
                    "characteristics": "$characteristics"
                }
            }
        ]

        a = self.collection.aggregate(pipeline)
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)

        for doc in a:
            result_text += f"Категория: {doc['category']}\n"
            result_text += f"Производитель: {doc['manufacturer']}\n"
            result_text += f"Модель: {doc['model']}\n"
            result_text += f"Цена: {doc['price']}\n"

            characteristics = doc.get('characteristics', {})
            if characteristics:
                result_text += "Характеристики:\n"
                for key, value in characteristics.items():
                    result_text += f"• {key}: {value}\n"

            result_text += SEPARATOR

        self.result_text.insert(tk.END, result_text)
        self.result_text.config(state="disabled")

    # 4 запрос
    def get_products_by_color(self):
        color = self.collection_var4.get()
        result_text = ""

        pipeline = [
            {
                "$match": {"characteristics.color": color}
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$category",
                    "model": "$model",
                    "manufacturer": "$manufacturer",
                    "price": "$price",
                }
            }
        ]

        a = self.collection.aggregate(pipeline)
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)

        for doc in a:
            result_text += f"Категория: {doc['category']}\n"
            result_text += f"Производитель: {doc['manufacturer']}\n"
            result_text += f"Модель: {doc['model']}\n"
            result_text += f"Цена: {doc['price']}\n"

            result_text += SEPARATOR

        self.result_text.insert(tk.END, result_text)
        self.result_text.config(state="disabled")

    def get_total_sold_amount(self):
        result_text = ""

        pipeline = [
            {
                "$match": {"customers": {"$exists": True}}
            },
            {
                "$group": {
                    "_id": None,
                    "total_sales": {"$sum": {"$multiply": ["$price", {"$size": "$customers"}]}}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "total_sales": 1
                }
            }
        ]

        cursor = self.collection.aggregate(pipeline)
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)

        for doc in cursor:
            total_sales = doc.get('total_sales', 0)
            result_text += f"{total_sales}\n"

        self.result_text.insert(tk.END, result_text)
        self.result_text.config(state="disabled")

    def get_products_count_by_category(self):
        result_text = ""

        pipeline = [
            {
                "$group": {
                    "_id": "$category",
                    "total_products": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$_id",
                    "total_products": 1
                }
            }
        ]

        a = self.collection.aggregate(pipeline)
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)

        for doc in a:
            result_text += f"Категория: {doc['category']}\n"
            result_text += f"Количество товаров: {doc['total_products']}\n"
            result_text += SEPARATOR

        self.result_text.insert(tk.END, result_text)
        self.result_text.config(state="disabled")

    def get_customer_names_by_product(self):
        category = self.collection_var7.get()
        result_text = ""

        pipeline = [
            {
                "$match": {"category": category, "customers": {"$exists": True}}
            },
            {
                "$group": {
                    "_id": "$customers.name"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "customer_names": "$_id"
                }
            }
        ]

        cursor = self.collection.aggregate(pipeline)
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)

        found_customers = False

        for doc in cursor:
            customer_names = doc.get('customer_names', [])
            for name in customer_names:
                result_text += f"• {name}\n"
                found_customers = True

        if not found_customers:
            result_text = f"Продаж товара '{category}' не было\n"

        self.result_text.insert(tk.END, result_text)
        self.result_text.config(state="disabled")

    def get_customer_names_by_product_and_delivery(self):
        category = self.collection_var8.get()
        method_obtaining = self.collection_var8_1.get()
        result_text = ""

        pipeline = [
            {
                "$match": {"category": category, "customers": {"$exists": True}}
            },
            {
                "$unwind": "$customers"
            },
            {
                "$match": {"customers.method_obtaining": method_obtaining}
            },
            {
                "$group": {
                    "_id": "$customers.name"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "customer_name": "$_id"
                }
            }
        ]

        cursor = self.collection.aggregate(pipeline)
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)

        found_customers = False

        for doc in cursor:
            json_str = doc["customer_name"]
            self.result_text.insert(tk.END, "• " + json_str + "\n")
            found_customers = True

        if not found_customers:
            self.result_text.insert(tk.END,
                                    f"Доставки товара '{category}' указанным способом '{method_obtaining}' не было\n")

        self.result_text.config(state="disabled")

    def update_result_text(self, text):
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")



root = tk.Tk()
app = ProductQueryApp(root, collection)
root.mainloop()

