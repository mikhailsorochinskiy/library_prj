# Используем официальный легкий образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости для PostgreSQL (нужны для psycopg2)
RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код проекта
COPY . .

# Собираем статические файлы (WhiteNoise их подхватит)
#RUN python manage.py collectstatic --noinput

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска сервера через Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]