import os
import asyncio
import logging

from tronpy import Tron
from tronpy.providers import HTTPProvider

logger = logging.getLogger(__name__)

API_KEY = os.getenv("API_KEY")

if API_KEY:
    client = Tron(HTTPProvider(api_key=API_KEY))
else:
    client = Tron()


def get_wallet_info_sync(address: str) -> dict:
    """
    Получает баланс указанного Tron-кошелька.

    Args:
        address (str): Tron-адрес кошелька.

    Returns:
        dict: Содержит address, bandwidth, energy и balance.
    """
    try:
        logger.debug(f"Запрос данных кошелька: {address}")
        account_info = client.get_account(address)
        resource_info = client.get_account_resource(address)
        logger.debug(f"Запрос данных кошелька успешен")
        return {
            "address": address,
            "bandwidth": resource_info.get("free_net_limit", 0),
            "energy": resource_info.get("energy_limit", 0),
            "balance": account_info.get("balance", 0) / 1_000_000
        }
    except Exception as e:
        logger.exception(f"Ошибка при получении данных для {address}: {e}")
        raise


async def get_wallet_info(address: str) -> dict:
    """
        Запускает синхронную функцию _sync_get_wallet_info для
        получения данных указанного Tron-кошелька.

        Args:
            address (str): Tron-адрес кошелька.

        Returns:
            dict: Содержит address, bandwidth, energy и balance.

        Raises:
            ValueError: Если адрес некорректен или результат не является словарём.

        """
    if not address.startswith("T"):
        logger.warning(f"Некорректный адрес Tron: {address}")
        raise ValueError(f"Invalid TRON address: {address}")

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, get_wallet_info_sync, address)

    if not isinstance(result, dict):
        logger.error(f"get_wallet_info_sync returned not a dict: {result} ({type(result)})")
        raise ValueError(f"get_wallet_info_sync returned not a dict: {result} ({type(result)})")

    return result
