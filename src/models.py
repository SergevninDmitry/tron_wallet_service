from src.db import Base

from sqlalchemy import Column, Integer, String, Float


class WalletRequest(Base):
    __tablename__ = "wallet_request"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False, index=True)
    bandwidth = Column(Integer, nullable=False)
    energy = Column(Integer, nullable=False)
    balance = Column(Float, nullable=False)
