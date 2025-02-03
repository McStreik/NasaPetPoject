import pandas as pd
import sqlite3
import json

# Читаем JSON
with open("nasa_apod.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

    df_json = pd.DataFrame(json_data)

# Читаем SQLite
conn = sqlite3.connect("nasa_data.db")
df_sql = pd.read_sql("SELECT * FROM nasa_apod", conn)
conn.close()

# Анализируем данные
print("\nКоличество записей в JSON:", len(df_json))
print("\nКоличество записей в SQLite:", len(df_sql))

print("\nСтатистика по длинне описания (SQLite):")
print(df_sql["explanation_length"].describe())

# Фильтр записей с длинными описаниями

long_explanation = df_sql[df_sql["explanation_length"] > 200]
print("\nЗаписи с длинными описаниями:")
print(long_explanation)
