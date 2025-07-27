import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.client import get_wallet_info
from src.models import WalletRequest
from src.repositories import WalletRepository

logger = logging.getLogger(__name__)


class WalletService:
    """
    Сервис для управления Tron-кошельками:
    - Получение информации о кошельке через Tron API
    - Сохранение в БД
    - Получение списка сохранённых кошельков
    """
    def __init__(self, session: AsyncSession):
        self.repo = WalletRepository(session)

    async def create_wallet(self, address: str) -> WalletRequest:
        try:
            data = await get_wallet_info(address)
        except ValueError as e:
            logger.warning(f"Некорректный адрес или ошибка Tron API: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.exception(f"Непредвиденная ошибка при создании кошелька: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

        wallet = WalletRequest(**data)
        saved_wallet = await self.repo.add(wallet)
        logger.info(f"Информация кошелька сохранена в БД: {saved_wallet.address}")
        return saved_wallet

    async def get_wallets(self, skip: int = 0, limit: int = 10) -> List[WalletRequest]:
        logger.debug(f"Получение кошельков из БД: skip={skip}, limit={limit}")
        return await self.repo.list(skip=skip, limit=limit)
