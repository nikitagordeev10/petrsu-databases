import pymongo
import json

# Подключение
client = pymongo.MongoClient('localhost')
database = client['22307']

# Создание коллекции
collection = database["online_store"]


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
                "category": "Смартфон",
                "manufacturer": "Apple",
                "model": "iPhone 13",
                "price": 70000,
                "characteristics": {
                    "display": "6.1 inches",
                    "camera": "12 MP",
                    "storage": "256 GB",
                    "color": "белый"
                },
                "customers": [
                    {
                        "name": "Анна",
                        "purchase_date": "02.12.2023",
                        "review": "iOS просто волшебство, камера поражает качеством снимков!",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Петр",
                        "purchase_date": "14.10.2023",
                        "review": "Дороговато, но стоит каждого рубля",
                        "star_count": "4",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Телефон",
                "manufacturer": "Xiaomi",
                "model": "Redmi Note 10",
                "price": 18000,
                "characteristics": {
                    "display": "6.43 inches",
                    "camera": "48 MP",
                    "storage": "128 GB",
                    "color": "красный"
                },
                "customers": [
                    {
                        "name": "Дмитрий",
                        "purchase_date": "20.11.2023",
                        "review": "Отличный смартфон за свои деньги, всем рекомендую!",
                        "star_count": "5",
                        "method_obtaining": "Доставка"
                    },
                    {
                        "name": "Ольга",
                        "purchase_date": "03.09.2023",
                        "review": "Батарея держит долго, удобный интерфейс",
                        "star_count": "4",
                        "method_obtaining": "Доставка"
                    }
                ]
            },

            {
                "category": "Телефон",
                "manufacturer": "OnePlus",
                "model": "9 Pro",
                "price": 48000,
                "characteristics": {
                    "display": "6.7 inches",
                    "camera": "48 MP",
                    "storage": "256 GB",
                    "color": "желтый"
                },
                "customers": [
                    {
                        "name": "Сергей",
                        "purchase_date": "12.12.2023",
                        "review": "Мощный аппарат, отличная камера, все, что нужно!",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Наталья",
                        "purchase_date": "28.09.2023",
                        "review": "Достойная альтернатива флагманам других брендов",
                        "star_count": "4",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Смартфон",
                "manufacturer": "Huawei",
                "model": "P40 Lite",
                "price": 23000,
                "characteristics": {
                    "display": "6.4 inches",
                    "camera": "48 MP",
                    "storage": "128 GB",
                    "color": "белый"
                },
                "customers": [
                    {
                        "name": "Михаил",
                        "purchase_date": "08.11.2023",
                        "review": "Хороший смартфон за разумные деньги",
                        "star_count": "5",
                        "method_obtaining": "Доставка"
                    },
                    {
                        "name": "Алина",
                        "purchase_date": "19.09.2023",
                        "review": "Стильный дизайн, удобное управление",
                        "star_count": "4",
                        "method_obtaining": "Доставка"
                    }
                ]
            },

            {
                "category": "Ноутбук",
                "manufacturer": "ASUS",
                "model": "ROG Strix G15",
                "price": 104000,
                "characteristics": {
                    "processor": "Intel i7",
                    "RAM": "16 GB",
                    "storage": "512 GB SSD",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Алексей",
                        "purchase_date": "15.12.2023",
                        "review": "Мощный ноутбук!",
                        "star_count": "5",
                        "method_obtaining": "СДЭК"
                    },
                    {
                        "name": "Мария",
                        "purchase_date": "23.11.2023",
                        "review": "Кошмар, стоит как боинг!",
                        "star_count": "2",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Ноутбук",
                "manufacturer": "Lenovo",
                "model": "Legion 5",
                "price": 90000,
                "characteristics": {
                    "processor": "AMD Ryzen 7",
                    "RAM": "16 GB",
                    "storage": "1 TB SSD",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Михаил",
                        "purchase_date": "15.02.2022",
                        "review": "Идеальный выбор для геймеров, отличная производительность",
                        "star_count": "5",
                        "method_obtaining": "СДЭК"
                    },
                    {
                        "name": "Екатерина",
                        "purchase_date": "23.01.2022",
                        "review": "Стильный дизайн, удобная клавиатура",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Ноутбук",
                "manufacturer": "Acer",
                "model": "Predator Helios 300",
                "price": 110000,
                "characteristics": {
                    "processor": "Intel Core i7",
                    "RAM": "16 GB",
                    "storage": "512 GB SSD",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Ольга",
                        "purchase_date": "20.03.2022",
                        "review": "Отличное охлаждение, игры идут без тормозов",
                        "star_count": "5",
                        "method_obtaining": "Доставка"
                    },
                    {
                        "name": "Сергей",
                        "purchase_date": "08.02.2022",
                        "review": "Цена немного кусается, но игровой опыт впечатляет",
                        "star_count": "4",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Ноутбук",
                "manufacturer": "HP",
                "model": "Omen 15",
                "price": 98000,
                "characteristics": {
                    "processor": "AMD Ryzen 5",
                    "RAM": "8 GB",
                    "storage": "256 GB SSD",
                    "color": "белый"
                },
                "customers": [
                    {
                        "name": "Ирина",
                        "purchase_date": "12.04.2024",
                        "review": "Доступный геймерский ноутбук, отличное соотношение цена-качество",
                        "star_count": "5",
                        "method_obtaining": "СДЭК"
                    },
                    {
                        "name": "Александр",
                        "purchase_date": "01.03.2024",
                        "review": "Не самый мощный, но для своей цены отличный вариант",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Телевизор",
                "manufacturer": "LG",
                "model": "OLED55CX",
                "price": 56000,
                "characteristics": {
                    "size": "55 inches",
                    "resolution": "4K",
                    "smartTV": "true",
                    "color": "белый"
                },
                "customer_info": [
                    {
                        "name": "Анна",
                        "purchase_date": "25.01.2023",
                        "review": "Цвет отличается от того что на фото",
                        "star_count": "2",
                        "method_obtaining": "СДЭК"
                    },
                    {
                        "name": "Артем",
                        "purchase_date": "02.01.2023",
                        "review": "Удобный и стильный, хорошая цена",
                        "star_count": "5",
                        "method_obtaining": "Самвывоз"
                    }
                ]
            },
            {
                "category": "Фотоаппарат",
                "manufacturer": "Canon",
                "model": "EOS Rebel T7",
                "price": 56000,
                "characteristics": {
                    "megapixels": 24,
                    "zoom": "10x",
                    "shootingModes": ["Auto", "Manual"],
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Владимир",
                        "purchase_date": "05.09.2023",
                        "review": "Отличное соотношение цена-качество",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Екатерина",
                        "purchase_date": "05.03.2023",
                        "review": "Стильный дизайн, плохой аккумулятор",
                        "star_count": "4",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Фотоаппарат",
                "manufacturer": "Nikon",
                "model": "D5600",
                "price": 65000,
                "characteristics": {
                    "megapixels": 24.2,
                    "zoom": "3.2x",
                    "shootingModes": ["Auto", "Program", "Manual"],
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Андрей",
                        "purchase_date": "12.11.2023",
                        "review": "Отличный выбор для начинающих и опытных фотографов",
                        "star_count": "5",
                        "method_obtaining": "Доставка"
                    },
                    {
                        "name": "Ольга",
                        "purchase_date": "28.09.2023",
                        "review": "Удобное управление, качественные снимки",
                        "star_count": "4",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Наушники",
                "manufacturer": "Sony",
                "model": "WH-1000XM4",
                "price": 25000,
                "characteristics": {
                    "type": "Bluetooth",
                    "noise_cancellation": "true",
                    "battery_life": "30 hours",
                    "color": "серый"
                },
                "customers": [
                    {
                        "name": "Андрей",
                        "purchase_date": "12.08.2023",
                        "review": "Прекрасное шумоподавление, отличное качество звука",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Ольга",
                        "purchase_date": "18.05.2023",
                        "review": "Удобные, но дорогие",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Кофемашина",
                "manufacturer": "De'Longhi",
                "model": "ECAM 22.110.B",
                "price": 90000,
                "characteristics": {
                    "type": "Автоматическая",
                    "pressure": "15 бар",
                    "capacity": "1.8 литра",
                    "color": "серебристый"
                },
                "customers": [
                    {
                        "name": "Наталия",
                        "purchase_date": "08.07.2023",
                        "review": "Лучшая кофемашина, которую я когда-либо имела",
                        "star_count": "5",
                        "method_obtaining": "СДЭК"
                    },
                    {
                        "name": "Денис",
                        "purchase_date": "15.04.2023",
                        "review": "Неплохо, но сложно чистить",
                        "star_count": "3",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Электрический самокат",
                "manufacturer": "Xiaomi",
                "model": "Mi Electric Scooter",
                "price": 18000,
                "characteristics": {
                    "maxSpeed": "25 km/h",
                    "range": "30 km",
                    "weightLimit": "100 kg",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Сергей",
                        "purchase_date": "02.09.2023",
                        "review": "Отличный способ передвижения в городе!",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Марина",
                        "purchase_date": "10.08.2023",
                        "review": "Быстро разряжается, но удобен для коротких поездок",
                        "star_count": "3",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Стиральная машина",
                "manufacturer": "Bosch",
                "model": "Serie 6",
                "price": 40000,
                "characteristics": {
                    "capacity": "8 кг",
                    "spinSpeed": "1400 об/мин",
                    "programs": ["Cotton", "Synthetics", "Wool"],
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Елена",
                        "purchase_date": "20.11.2023",
                        "review": "Эффективная и тихая стиральная машина",
                        "star_count": "5",
                        "method_obtaining": "СДЭК"
                    },
                    {
                        "name": "Игорь",
                        "purchase_date": "05.11.2023",
                        "review": "Проста в использовании, но дороговата",
                        "star_count": "4",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Игровая консоль",
                "manufacturer": "Sony",
                "model": "PlayStation 5",
                "price": 50000,
                "characteristics": {
                    "storage": "825 GB SSD",
                    "resolution": "4K",
                    "frameRate": "120 fps",
                    "color": "белый"
                },
                "customers": [
                    {
                        "name": "Александр",
                        "purchase_date": "07.06.2023",
                        "review": "Лучшая игровая консоль на рынке!",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Татьяна",
                        "purchase_date": "15.02.2023",
                        "review": "Ждать стоило, невероятная графика",
                        "star_count": "5",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Гироскутер",
                "manufacturer": "Segway",
                "model": "Ninebot S",
                "price": 30000,
                "characteristics": {
                    "maxSpeed": "16 km/h",
                    "range": "25 km",
                    "weightLimit": "100 kg",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Павел",
                        "purchase_date": "05.07.2023",
                        "review": "Веселая альтернатива для перемещения по городу",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Светлана",
                        "purchase_date": "10.05.2023",
                        "review": "Сложно управлять, но забавно",
                        "star_count": "3",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Микроволновая печь",
                "manufacturer": "Panasonic",
                "model": "NN-ST34HM",
                "price": 8000,
                "characteristics": {
                    "capacity": "23 литра",
                    "power": "800 Вт",
                    "control": "электронное",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Тимур",
                        "purchase_date": "15.10.2023",
                        "review": "Проста в использовании, греет быстро",
                        "star_count": "4",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Ангелина",
                        "purchase_date": "22.09.2023",
                        "review": "Неплохая, но сложное управление",
                        "star_count": "3",
                        "method_obtaining": "СДЭК"
                    }
                ]
            },

            {
                "category": "Видеокамера",
                "manufacturer": "GoPro",
                "model": "HERO9 Black",
                "price": 35000,
                "characteristics": {
                    "resolution": "5K",
                    "fps": "30",
                    "waterproof": "true",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Алина",
                        "purchase_date": "02.11.2023",
                        "review": "Прекрасное качество видео, удобно использовать",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Дмитрий",
                        "purchase_date": "10.10.2023",
                        "review": "Дорого, но стоит своих денег",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Блендер",
                "manufacturer": "Bosch",
                "model": "SilentMixx Pro",
                "price": 5000,
                "characteristics": {
                    "power": "800 Вт",
                    "speeds": "3",
                    "jar_сapacity": "1.5 литра",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Михаил",
                        "purchase_date": "05.06.2023",
                        "review": "Тихий и мощный блендер",
                        "star_count": "5",
                        "method_obtaining": "СДЭК"
                    },
                    {
                        "name": "Елена",
                        "purchase_date": "12.02.2023",
                        "review": "Недорогой, но не очень удобный",
                        "star_count": "3",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Пылесос",
                "manufacturer": "Dyson",
                "model": "V11 Absolute",
                "price": 40000,
                "characteristics": {
                    "suctionPower": "185 АВт",
                    "binCapacity": "0.76 литра",
                    "battery_life": "60 минут",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Александра",
                        "purchase_date": "15.05.2023",
                        "review": "Мощный пылесос, удобно использовать",
                        "star_count": "5",
                        "method_obtaining": "СДЭК"
                    },
                    {
                        "name": "Иван",
                        "purchase_date": "22.04.2023",
                        "review": "Дорого, но оправдывает свою цену",
                        "star_count": "4",
                        "method_obtaining": "Самовывоз"
                    }
                ]
            },

            {
                "category": "Монитор",
                "manufacturer": "Dell",
                "model": "UltraSharp U2720Q",
                "price": 30000,
                "characteristics": {
                    "size": "27 inches",
                    "resolution": "4K",
                    "refreshRate": "60 Гц",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Сергей",
                        "purchase_date": "12.08.2023",
                        "review": "Отличный монитор для работы и игр",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Анна",
                        "purchase_date": "05.07.2023",
                        "review": "Яркие цвета, удобный в использовании",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Кофеварка",
                "manufacturer": "De'Longhi",
                "model": "Dedica Style EC 685",
                "price": 15000,
                "characteristics": {
                    "type": "Эспрессо",
                    "pressure": "15 бар",
                    "capacity": "1 литр",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Мария",
                        "purchase_date": "27.07.2023",
                        "review": "Отличный кофе, проста в использовании",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Артем",
                        "purchase_date": "09.08.2022",
                        "review": "Стильный дизайн, но сложно чистить",
                        "star_count": "3",
                        "method_obtaining": "СДЭК"
                    }
                ]
            },

            {
                "category": "Портативная колонка",
                "manufacturer": "JBL",
                "model": "Charge 4",
                "price": 8000,
                "characteristics": {
                    "power": "30 Вт",
                    "battery_life": "20 часов",
                    "waterproof": "true",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Екатерина",
                        "purchase_date": "09.05.2022",
                        "review": "Отличное качество звука, удобно брать с собой",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Алексей",
                        "purchase_date": "09.01.2022",
                        "review": "Долго держит заряд, устойчива к влаге",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Электрическая зубная щетка",
                "manufacturer": "Oral-B",
                "model": "Pro 700",
                "price": 3000,
                "characteristics": {
                    "brushingModes": ["ежедневная чистка", "очищение десен", "чувствительные десны"],
                    "timer": "true",
                    "battery_life": "10 дней",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Антонина",
                        "purchase_date": "10.01.2023",
                        "review": "Отлично чистит зубы, удобно использовать",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Петр",
                        "purchase_date": "18.02.2023",
                        "review": "Немного дороговата, но стоит своих денег",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Фитнес-браслет",
                "manufacturer": "Xiaomi",
                "model": "Mi Band 6",
                "price": 5500,
                "characteristics": {
                    "screen_size": "1.56 дюйма",
                    "heart_rate_monitor": "true",
                    "water_resistance": "5 ATM",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Максим",
                        "purchase_date": "05.03.2023",
                        "review": "Отличный браслет для отслеживания активности",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Ольга",
                        "purchase_date": "12.04.2023",
                        "review": "Удобно носить, много полезных функций",
                        "star_count": "4",
                        "method_obtaining": "СДЭК"
                    }
                ]
            },
            {
                "category": "Компьютерная мышь",
                "manufacturer": "Logitech",
                "model": "MX Master 3",
                "price": 6000,
                "characteristics": {
                    "connectionType": "Bluetooth, USB",
                    "buttons": 7,
                    "sensor": "Darkfield High Precision",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Денис",
                        "purchase_date": "20.05.2023",
                        "review": "Отличная мышь для работы и игр",
                        "star_count": "5",
                        "method_obtaining": "СДЭК"
                    },
                    {
                        "name": "Алина",
                        "purchase_date": "28.06.2023",
                        "review": "Эргономичный дизайн, удобная в использовании",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Электрическая бритва",
                "manufacturer": "Philips",
                "model": "Series 9000",
                "price": 7000,
                "characteristics": {
                    "bladeType": "V-Track Precision",
                    "shavingHeads": 3,
                    "waterproof": "true",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Евгений",
                        "purchase_date": "15.07.2023",
                        "review": "Бреет близко, не раздражает кожу",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Наталья",
                        "purchase_date": "22.08.2023",
                        "review": "Немного громковата, но результат отличный",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },
            {
                "category": "Беспроводные наушники",
                "manufacturer": "Apple",
                "model": "AirPods Pro",
                "price": 20000,
                "characteristics": {
                    "noiseCancellation": "true",
                    "battery_life": "4.5 часа (без шумоподавления)",
                    "wirelessCharging": "true",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Ирина",
                        "purchase_date": "02.09.2023",
                        "review": "Отличное качество звука, удобно использовать",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Артем",
                        "purchase_date": "10.10.2023",
                        "review": "Дорого, но супер удобные",
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
                "customers": [
                    {
                        "name": "Нина",
                        "purchase_date": "20.03.2023",
                        "review": "Отличные часы для мониторинга здоровья",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Сергей",
                        "purchase_date": "28.04.2023",
                        "review": "Удобные, стильные, но дорогие",
                        "star_count": "4",
                        "method_obtaining": "Яндекс Доставка"
                    }
                ]
            },

            {
                "category": "Газонокосилка",
                "manufacturer": "Bosch",
                "model": "Rotak 370 ER",
                "price": 32000,
                "characteristics": {
                    "cuttingWidth": "37 см",
                    "cuttingHeight": "20-70 мм",
                    "grassBoxCapacity": "40 литров",
                    "color": "черный"
                },
                "customers": [
                    {
                        "name": "Татьяна",
                        "purchase_date": "10.05.2023",
                        "review": "Отличная газонокосилка, радует результат",
                        "star_count": "5",
                        "method_obtaining": "Самовывоз"
                    },
                    {
                        "name": "Владимир",
                        "purchase_date": "18.06.2023",
                        "review": "Легко косит газон, удобно использовать",
                        "star_count": "4",
                        "method_obtaining": "СДЭК"
                    }
                ]
            }

        ]

    collection.delete_many({})

    for document in shop_data:
        collection.insert_one(document)
    print(len(shop_data))

save_document()
