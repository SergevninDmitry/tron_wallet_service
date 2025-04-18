from .db import Base
from sqlalchemy import Column, Integer, String, Float


class WalletRequest(Base):
    __tablename__ = "wallet_request"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    balance = Column(Float)
