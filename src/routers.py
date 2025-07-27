from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import WalletRequestCreate, WalletRequestResponse
from src.services import WalletService
from src.db import get_db

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/wallets", response_model=WalletRequestResponse)
async def create_wallet(request: WalletRequestCreate, db: AsyncSession = Depends(get_db)):
    """
    Создает Tron-кошелек и получает информацию о балансе и ресурсах.

    Args:
        request (WalletRequestCreate): Данные с адресом Tron-кошелька.
        db (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        WalletResponse: Информация о кошельке.
    """
    service = WalletService(db)
    try:
        wallet = await service.create_wallet(request.address)
        logger.info(f"Создан кошелек: {wallet.address}")

    except Exception as e:
        logger.exception(f"Ошибка при создании кошелька: {e}")
        raise HTTPException(status_code=400, detail="Не удалось создать кошелек")
    return wallet


@router.get("/wallets", response_model=List[WalletRequestResponse])
async def list_wallets(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
        Получает все зарегистрированные обращения к Tron-кошельку с информацией о нем.

        Args:
            skip: Количество записей в бд, которые нужно пропустить.
            limit: Количество записей запрашиваемых их бд.
            db: AsyncSession: Сессия базы данных.

        Returns:
            List[WalletRequestResponse]: Список записей о Tron-кошельках.
        """
    service = WalletService(db)
    wallets = await service.get_wallets(skip, limit)
    return wallets


@router.get("/health", summary="Healthcheck endpoint")
async def healthcheck():
    return JSONResponse(content={"status": "ok"})
