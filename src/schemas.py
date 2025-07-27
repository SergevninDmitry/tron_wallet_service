from pydantic import BaseModel, Field


class WalletRequestCreate(BaseModel):
    address: str = Field(..., schema_extra={"example": "T..."})


class WalletRequestResponse(BaseModel):
    id: int
    address: str
    bandwidth: int
    energy: int
    balance: float

    model_config = {
        "from_attributes": True
    }
