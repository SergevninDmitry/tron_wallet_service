from fastapi.testclient import TestClient
from app.app import app
from app.db import SessionLocal
from app.models import WalletRequest
import pytest
from tronpy import Tron
from app.client import get_wallet_info
from sqlalchemy.orm import Session


@pytest.fixture(scope="module")
def test_db():
    db = SessionLocal()
    db.query(WalletRequest).delete()
    db.commit()
    yield db
    db.close()


@pytest.fixture
def client():
    client = TestClient(app)
    return client


def test_wallet_to_db(client, test_db):
    # tron_client = Tron(network='nile')
    # wallet = tron_client.generate_address()
    # print(wallet)
    # address = wallet['base58check_address']
    wallet_data = {"address": "TMnZSZHyNNKyyMJSC19Fjt8pT6fQHbriXz"}

    response = client.post("/wallets", json=wallet_data)

    assert response.status_code == 200
    response_data = response.json()

    assert response_data["address"] == wallet_data["address"]
    assert "bandwidth" in response_data
    assert "energy" in response_data
    assert "balance" in response_data

    db_wallet = test_db.query(WalletRequest).filter(WalletRequest.address == wallet_data["address"]).first()
    assert db_wallet is not None
    assert db_wallet.address == wallet_data["address"]


def test_wallet_info_to_db(test_db: Session):
    # tron_client = Tron(network='nile')
    # wallet = tron_client.generate_address()
    address = "TMnZSZHyNNKyyMJSC19Fjt8pT6fQHbriXz"
    wallet_data = get_wallet_info(address)

    wallet = WalletRequest(**wallet_data)
    test_db.add(wallet)
    test_db.commit()
    test_db.refresh(wallet)

    db_wallet = test_db.query(WalletRequest).filter(WalletRequest.address == address).first()
    assert db_wallet is not None
    assert db_wallet.address == address
    assert db_wallet.bandwidth == wallet_data["bandwidth"]
    assert db_wallet.energy == wallet_data["energy"]
    assert db_wallet.balance == wallet_data["balance"]
