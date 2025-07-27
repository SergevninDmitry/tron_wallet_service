# Tron Wallet Service

Проект представляет собой REST API сервис на FastAPI для работы с Tron-кошельками:  
- Получение баланса и ресурсов Tron-кошелька по адресу через API Tron  
- Сохранение информации в PostgreSQL базу данных  
- Запрос списка сохранённых кошельков  

---

## Переменные окружения

В проекте используется файл `.env` с такими ключами:  

```dotenv
API_KEY=your_api_key_here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=tron_wallet
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/tron_wallet
TEST_ADDRESS=your-test-address-here
TEST_DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/tron_wallet_test
```
Где API_KEY - бесплатный API Key с сайта https://www.trongrid.io, TEST_ADDRESS - пример существующего адреса для тестирования приложения
Скопируйте `.env.example` в `.env` и заполните нужные значения.

---

## Запуск сервиса с Docker Compose

1. Соберите и запустите контейнеры:

```bash
docker-compose up --build
```
2. Сервис будет доступен по адресу: http://localhost:8000

---
## API Эндпоинты

- `POST /wallets` — Создать запись кошелька по адресу и получить баланс с ресурсами  
- `GET /wallets` — Получить список сохранённых кошельков с пагинацией  
- `GET /health` — Проверка работоспособности сервера (возвращает статус "ok")  
### Пример запроса `POST /wallets`
```json
{
  "address": "TY6RiRYkYhCo7VHxRseFE3dxZKT3wm6dWh"
}
```
### Пример ответа
```json
{
  "id": 1,
  "address": "TY6RiRYkYhCo7VHxRseFE3dxZKT3wm6dWh",
  "bandwidth": 0,
  "energy": 0,
  "balance": 84.611004
}
```
---

## Запуск тестов


Для запуска тестов используй эти команды:
```bash
docker exec -it tron_wallet_service-db-1 psql -U postgres -c "CREATE DATABASE tron_wallet_test;"
docker exec -it tron_wallet_service-web-1 sh -c "PYTHONPATH=/app pytest -v tests"
```