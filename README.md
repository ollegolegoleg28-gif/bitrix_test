# Bitrix24 Data Import and Flask Web App

## Ссылка на работающий сервер
[http://135.181.101.209:5000/](http://135.181.101.209:5000/)

## Краткое описание

### 1. Выбранная конфигурация Hetzner
- Сервер: Hetzner Cloud, стандартный VPS.
- Обоснование: достаточные ресурсы для тестового проекта (1 CPU, 2GB RAM, 20GB SSD), минимальные затраты.
- ОС: Ubuntu 24.04 LTS.

### 2. Что установлено и запущено на сервере
- Python 3.12 с виртуальным окружением `venv`.
- Flask для веб-интерфейса.
- PostgreSQL для хранения данных.
- Приложение Flask запущено как сервис через `systemd`, доступно по `http://135.181.101.209:5000`.

### 3. Как были получены и сохранены данные из Bitrix24
- Скрипт `fetch_data.py` подключается к Bitrix24 REST API и выгружает ключевые сущности: Лиды, Сделки, Контакты.
- Данные сохраняются в JSON файлы (`contacts.json`, `leads.json`, `deals.json`).
- Скрипт `import_to_postgres.py` импортирует JSON данные в PostgreSQL с минимальной схемой БД.

### 4. Схема базы данных (ER-диаграмма)
contacts

id SERIAL PRIMARY KEY
name TEXT NOT NULL
phone TEXT
email TEXT

leads

id SERIAL PRIMARY KEY
title TEXT NOT NULL
status TEXT
created_date TIMESTAMP
contact_id INT REFERENCES contacts(id) ON DELETE SET NULL

deals

id SERIAL PRIMARY KEY
title TEXT NOT NULL
stage TEXT
opportunity NUMERIC(12,2)
contact_id INT REFERENCES contacts(id) ON DELETE SET NULL


## Репозиторий с кодом и реализацией
[GitHub Repository](https://github.com/ollegolegoleg28-gif/bitrix_test)

### Что в репозитории
- `fetch_data.py` — скрипт получения данных через REST API Bitrix24.
- `import_to_postgres.py` — импорт JSON данных в PostgreSQL.
- `web/` — Flask веб-приложение с минимальным интерфейсом:
  - `app.py` — основной файл приложения
  - `templates/index.html` — страница отображения данных
  - `requirements.txt` — зависимости Python
- JSON файлы с данными: `contacts.json`, `leads.json`, `deals.json`.

---

### Инструкция по запуску
1. Установить зависимости: `pip install -r requirements.txt`.
2. Создать базу данных и таблицы PostgreSQL (скрипт `import_to_postgres.py` сам проверяет таблицы).
3. Запустить Flask:
```bash
export FLASK_APP=web/app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000

или через systemd-сервис (создаем unit-file) для постоянной работы

[Unit]
Description=Bitrix Flask Web Application
After=network.target postgresql.service

[Service]
User=root
WorkingDirectory=/root/bitrix_project/web
Environment="FLASK_APP=app.py"
Environment="FLASK_ENV=production"
Environment="PATH=/root/bitrix_project/venv/bin"
ExecStart=/root/bitrix_project/venv/bin/flask run --host=0.0.0.0 --port=5000
Restart=always

[Install]
WantedBy=multi-user.target
