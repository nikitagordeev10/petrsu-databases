import pymongo
import json

# Подключение
client = pymongo.MongoClient('localhost')
database = client['22307']

# Создание коллекции
collection = database["small_online_store"]


def save_document():
    shop_data = \
        [
            {
                "category": "Смартфон",
                "manufacturer": "Samsung",
                "model": "Galaxy S21",
                "price": 35000,
                "characteristics": {
                    "display": "6.2 inches",
                    "camera": "12 MP",
                    "storage": "64 GB",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Иван",
                        "purchase_date": "15.10.2023",
                        "review": "Отличный смартфон!",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Мария",
                        "purchase_date": "23.08.2023",
                        "review": "Покупкой довольна, но зарядки в комплекте нет",
                        "star_count": "4",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Мобильный телефон",
                "manufacturer": "Samsung",
                "model": "Galaxy A52",
                "price": 25000,
                "characteristics": {
                    "display": "6.5 inches",
                    "camera": "64 MP",
                    "storage": "128 GB",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Алексей",
                        "purchase_date": "05.11.2023",
                        "review": "Отличная камера, невероятная производительность!",
                        "star_count": "5",
                        "method_obtaining": "Почта России"
                    },
                    {
                        "name": "Екатерина",
                        "purchase_date": "18.09.2023",
                        "review": "Хорошее соотношение цена-качество, быстрая доставка",
                        "star_count": "4",
                        "method_obtaining": "СДЭК"
                    }
                ]
            },

            {
                "category": "Смарт-часы",
                "manufacturer": "Samsung",
                "model": "Galaxy Watch 4",
                "price": 18000,
                "characteristics": {
                    "display_type": "Super AMOLED",
                    "health_tracking": ["пульс", "сон", "шаги"],
                    "water_resistance": "5 ATM",
                    "color": "черный"
                },
            },

        ]

    collection.delete_many({})

    for document in shop_data:
        collection.insert_one(document)
    print(len(shop_data))

save_document()
