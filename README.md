# Сервис бронирования переговорных комнат

FastAPI приложение для бронирования переговорных комнат в коворкинге.

## Технологии

- Python 3.12
- FastAPI
- SQLAlchemy 2.0 (async)
- SQLite
- JWT аутентификация
- Poetry

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/fooga-Git/fastAPI_first_since.git
cd fastAPI_first_since

2. Установка зависимости

bash
poetry install --no-root

3. Настройка окружения
bash
echo 'SECRET_KEY=your-secret-key-here' > .env
echo 'ALGORITHM=HS256' >> .env
echo 'ACCESS_TOKEN_EXPIRE_MINUTES=480' >> .env
echo 'REFRESH_TOKEN_EXPIRE_DAYS=7' >> .env

4. Создание базы данных и первый запуск
bash
# Очистка старой БД (если есть)
rm -f *.db

# Создание супер админа
PYTHONPATH=. poetry run python app/scripts/create_super_admin.py

# Запуск сервера
poetry run uvicorn app.main:app --reload

5. Сброс пароля супер админа
bash
PYTHONPATH=. poetry run python app/scripts/reset_super_admin_password.py

## API документация
- `Swagger UI: http://localhost:8000/docs

## Основные эндпоинты

**Аутентификация**

- `POST /auth/register` — регистрация сотрудника
- `POST /auth/login` — вход (JWT)
- `POST /auth/refresh` — обновление токенов
- `GET /users/me` — информация о себе

**Комнаты**

- `GET /rooms` — список комнат (залогиненные)
- `POST /rooms` — создать комнату (админ)
- `PATCH /rooms/{id}` — обновить комнату (админ)
- `DELETE /rooms/{id}` — удалить комнату (админ)
- `GET /rooms/{id}/slots` — слоты комнаты (залогиненные)

**Бронирования**

- `POST /bookings` — создать бронь (сотрудник)
- `GET /bookings` — список броней (сотрудник — свои, админ — все)
- `DELETE /bookings/{id}` — отменить бронь (сотрудник — свою, админ — любую)

**Администрирование**

- `POST /admin/set-role` — назначить роль (админ)
- `DELETE /admin/users/{id}` — удалить пользователя (админ)