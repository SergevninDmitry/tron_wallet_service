from fastapi import APIRouter, Depends, HTTPException
from .classes import WalletRequestCreate, WalletRequestResponse
from .db import get_db
from .models import WalletRequest
from .client import get_wallet_info
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/wallets", response_model=WalletRequestResponse)
def wallet_to_db(info: WalletRequestCreate, db: Session = Depends(get_db)):
    try:
        data = get_wallet_info(info.address)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Tron address")

    wallet = WalletRequest(**data)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    print(repr(wallet))
    return wallet


@router.get("/wallets", response_model=list[WalletRequestResponse])
def get_wallets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(WalletRequest).offset(skip).limit(limit).all()
