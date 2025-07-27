import os
import pytest

from src.models import WalletRequest
from sqlalchemy import select

TEST_ADDRESS = os.getenv("TEST_ADDRESS")

'''Запуск тестов:
docker exec -it tron_wallet_serves-db-1 psql -U postgres -c "CREATE DATABASE tron_wallet_test;"
docker exec -it tron_wallet_serves-web-1 sh -c "PYTHONPATH=/app pytest -v tests"
'''


@pytest.mark.asyncio
async def test_create_wallet_endpoint(client):
    response = await client.post("/wallets", json={"address": TEST_ADDRESS})
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == TEST_ADDRESS
    assert "bandwidth" in data
    assert "energy" in data
    assert "balance" in data


@pytest.mark.asyncio
async def test_create_wallet(session):
    wallet = WalletRequest(address=TEST_ADDRESS, balance=88.06, energy=0, bandwidth=0)
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)

    assert wallet.id is not None
    assert wallet.address == TEST_ADDRESS


@pytest.mark.asyncio
async def test_get_wallets_endpoint(client):
    await client.post("/wallets", json={"address": TEST_ADDRESS})

    response = await client.get("/wallets?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["address"] == TEST_ADDRESS


@pytest.mark.asyncio
async def test_get_wallets(session):
    wallet = WalletRequest(
        address=TEST_ADDRESS,
        balance=123,
        energy=456,
        bandwidth=789.0
    )
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)

    result = await session.execute(select(WalletRequest))
    wallets = result.scalars().all()
    assert len(wallets) == 1
    assert wallets[0].address == TEST_ADDRESS
