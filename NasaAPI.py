import requests
import json
import os
from datetime import datetime
import sqlite3
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NASA_API_KEY")
URL = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
FILE_PATH = "nasa_apod.json"

response = requests.get(URL)

if response.status_code == 200:
    data = response.json()

    # Трансформация данных

    # Изменение формата даты
    data["date"] = datetime.strptime(data["date"], "%Y-%m-%d").strftime("%d.%m.%Y")

    # Органичение длинны описания
    data["explanation"] = (
        data["explanation"][:200] + "..."
        if len(data["explanation"]) > 200
        else data["explanation"]
    )

    # Добавление нового поля с длиной описания
    data["explanation_length"] = len(data["explanation"])

    # Оставляем только нужные поля

    transformed_data = {
        "date": data["date"],
        "title": data["title"],
        "url": data["url"],
        "explanation": data["explanation"],
        "explanation_length": data["explanation_length"],
    }

    # Подключаемся к базе (если файла нет, SQLite создаст его)
    conn = sqlite3.connect("nasa_data.db")
    cursor = conn.cursor()

    # Создаем таблицу, если ее еще нет
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS nasa_apod (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT,
                   title TEXT,
                   url TEXT,
                   explanation TEXT,
                   explanation_length UNTEGER
        )
                   
    """
    )
    conn.commit()
    conn.close()

    # Сохранение данных

    # Подключаемся к базе
    conn = sqlite3.connect("nasa_data.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM nasa_apod WHERE date = ?", (transformed_data["date"],)
    )
    existing_record = cursor.fetchone()

    # Вставляем данные в таблицу и проверяем на наличие дубликатов
    if existing_record:
        print("Данные за эту дату уже существуют, запись пропущена.")
    else:
        cursor.execute(
            """
            INSERT INTO nasa_apod (date, title, url, explanation, explanation_length)
            VALUES(?, ?, ?, ?, ?)
        """,
            (
                transformed_data["date"],
                transformed_data["title"],
                transformed_data["url"],
                transformed_data["explanation"],
                transformed_data["explanation_length"],
            ),
        )

        conn.commit()
        print("Новая запись добавлена в базу данных")
    conn.close()

    # Загружаем существующие данные, если файл JSON уже есть
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Проверяем, есть ли запись на эту дату
    if any(entry["date"] == transformed_data["date"] for entry in existing_data):
        print("Данные за эту дату уже есть в JSON, запись пропущена.")
    else:
        existing_data.append(transformed_data)

        # Перезаписываем файл с обновленными данными
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4)

        print("Данные сохранены в", FILE_PATH)


else:
    print(f"Ошибка: {response.status_code}")
