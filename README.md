# Booking Service — сервис бронирования переговорных комнат

Сервис для автоматизации бронирования переговорных комнат в коворкинге.  
Сотрудники могут просматривать доступность комнат, создавать и отменять свои бронирования.  
Администраторы могут управлять любыми бронированиями.

👨‍💻 Автор
Суродин Денис Эдуардович https://github.com/fooga-Git


## 🛠 Технологии

- **Python** 3.12
- **FastAPI** — веб-фреймворк
- **Poetry** — управление зависимостями
- **PostgreSQL** — база данных для `docker-compose.yml` 
- **SQLite** — база данныз для локальной работы
- **SQLAlchemy** (async) — ORM
- **JWT** — аутентификация
- **Docker** / **Docker Compose** — контейнеризация

## 👑 Супер админ

**Логин:** `admin`  
**Пароль:** `admin123`

> **⚠️ Внимание:** В учебном проекте пароль указан в документации для удобства проверяющих.  
> **В реальном проекте** пароль никогда не хранится в коде или README, а задаётся через переменные окружения или менеджеры секретов.
> **При запуске сервера локально и через Docker Супер админ создаётся автоматически.

                                            ** Локальная разработка **

1. Клонирование репозитория
```bash
git clone https://github.com/fooga-Git/fastAPI_first_since.git
cd fastAPI_first_since

2. Установка зависимостей
```bash
poetry install

3. Запуск сервера
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

4. Тестирование с помощью библиотеки pytest
```bash
poetry run pytest -v

5. Проверка API
Открой в браузере: http://localhost:8001/docs

База данных: SQLite (файл booking.db)

                                            ## 🐳 Запуск через Docker
                                        Способ 1: `docker run`  (Sqlite)
```bash
# Сборка образа
docker build -t booking-service:latest .

# Запуск контейнера (Sqlite)
docker run -d \
  --name booking-app \
  -p 8000:8000 \
  -e DATABASE_URL="sqlite:///./booking.db" \
  booking-service:latest

Открой в браузере: http://localhost:8000/docs

# Остановка и удаление контейнера
docker stop booking-app
docker rm booking-app

                                        Способ 2: `docker-compose up`  (PostgreSQL)
```bash
# Запуск контейнеров (PostgreSQL + приложение)
docker-compose up -d

# Проверка статуса контейнеров
docker ps

# Просмотр логов приложения
docker-compose logs app

# Проверка работоспособности
Открой в браузере: http://localhost:8000/docs

# Остановка и удаление всех контейнеров и volumes
docker-compose down -v
