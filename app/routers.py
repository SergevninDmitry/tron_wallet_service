from fastapi import APIRouter
from .classes import WalletRequestCreate, WalletRequestResponse
from .db import get_db
from .models import WalletRequest
from .client import get_wallet_info

router = APIRouter()
db = get_db()


@router.post("/wallet-info", response_model=WalletRequestResponse)
def wallet_to_db(info: WalletRequestCreate):
    return WalletRequestResponse(
        id=1,
        address="post TXYZ...",
        bandwidth=33,
        energy=123,
        balance=3.1,
        timestamp="2025"
    )
    # try:
    #     data = get_wallet_info(info.address)
    # except Exception as e:
    #     raise Exception(e, "Invalid Tron address")


@router.get("/wallet-info", response_model=WalletRequestResponse)
def get_wallets(skip: int = 0, limit: int = 10):
    return WalletRequestResponse(
        id=1,
        address="get TXYZ...",
        bandwidth=33,
        energy=123,
        balance=3.1,
        timestamp="2025"
    )
    # return db.query(WalletRequest).offset(skip).limit(limit).all()
