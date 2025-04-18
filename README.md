# FastAPI Tron Wallet Microservice

Этот микросервис позволяет получать информацию о кошельках Tron, сохранять их в базу данных и получать их список.


## Установка
```bash
git clone https://github.com/SergevninDmitry/tron_wallet_service.git
cd tron_wallet_service
```
### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Запуск приложения
```bash
uvicorn app.app:app --host localhost --port 8000
```
### Запуск тестов
```bash
python -m pytest -v
```
