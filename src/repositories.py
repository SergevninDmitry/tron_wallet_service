from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import WalletRequest
from typing import List
import logging

logger = logging.getLogger(__name__)


class WalletRepository:
    """
    Репозиторий для работы с WalletRequest.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, wallet: WalletRequest) -> WalletRequest:
        """
        Добавить новый кошелёк в базу данных.
        """
        try:
            self.session.add(wallet)
            await self.session.commit()
            await self.session.refresh(wallet)
            logger.info(f"Кошелёк добавлен: {wallet.address}")
            return wallet
        except Exception:
            await self.session.rollback()
            logger.exception("Ошибка при добавлении кошелька в БД")
            raise

    async def list(self, skip: int = 0, limit: int = 10) -> List[WalletRequest]:
        """
        Получить список кошельков с пагинацией.
        """
        logger.debug(f"Получение списка кошельков: skip={skip}, limit={limit}")
        result = await self.session.execute(
            select(WalletRequest).offset(skip).limit(limit)
        )
        wallets = result.scalars().all()
        logger.debug(f"Найдено {len(wallets)} кошельков")
        return wallets
