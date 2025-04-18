from pydantic import BaseModel, Field


class WalletRequestCreate(BaseModel):
    address: str = Field(..., example="TXYZ...")


class WalletRequestResponse(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance: float

    class Config:
        orm_mode = True
