from .db import Base
from sqlalchemy import Column, Integer, String


class WalletRequest(Base):
    __tablename__: str = "wallet_request"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
