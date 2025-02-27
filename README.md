ETL-пайплайн для NASA APOD

Этот проект — ETL-пайплайн, который автоматически загружает данные из API NASA APOD, сохраняет их локально и анализирует с помощью Pandas.

🚀 Функции проекта

✔️ Извлечение данных (Extract): Запрос данных из NASA APOD API
✔️ Трансформация (Transform): Обработка данных и удаление дубликатов
✔️ Загрузка (Load): Сохранение данных в SQLite и JSON
✔️ Анализ (Analyze): Использование Pandas для анализа данных

📂 Структура проекта

/ETL-Pipeline
│── NasaAPI.py        # Основной ETL-скрипт
│── analyze.py       # Анализ данных с Pandas
│── nasa_apod.json   # Локальное хранилище данных
│── nasa_data.db     # База данных SQLite
│── .env             # Файл с API-ключом (не коммитится)
│── .gitignore       # Игнорируемые файлы
│── README.md        # Описание проекта

🛠 Как запустить?
 1. Установите зависимости

pip install -r requirements.txt


 2. Создайте .env файл с API-ключом:

NASA_API_KEY=ваш_ключ


 3. Запустите ETL-пайплайн:

python NasaAPI.py


 4. Для анализа данных используйте:

python analyze.py



🤖 Автоматизация

Можно настроить автоматический запуск ETL-пайплайна с помощью Task Scheduler (Windows) или cron (Linux/MacOS).
