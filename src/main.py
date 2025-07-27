import os
import asyncio
import logging
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI

from src import models, db, routers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("tron_wallet_service")


async def _wait_for_db():
    """
    Ожидает доступности базы данных перед запуском приложения.
    """
    raw_url = os.getenv("DATABASE_URL")
    if not raw_url:
        logger.critical("DATABASE_URL не задан в окружении!")
        raise RuntimeError("DATABASE_URL is not set")

    asyncpg_url = raw_url.replace("postgresql+asyncpg://", "postgresql://", 1)

    while True:
        try:
            conn = await asyncpg.connect(asyncpg_url)
            await conn.close()
            logger.info("Успешно подключились к базе данных.")
            break
        except Exception as e:
            logger.warning(f"Ожидание базы данных: {e}")
            await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения Tron Wallet Service...")
    await _wait_for_db()

    logger.info("Создание таблиц в базе данных...")
    async with db.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    logger.info("Приложение инициализировано.")
    yield
    logger.info("Приложение завершает работу.")


app = FastAPI(title="Tron Wallet Service", lifespan=lifespan)

app.include_router(routers.router)
