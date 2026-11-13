from fastapi import FastAPI
from pydantic import BaseModel, Field

from .scoring import WalletStats, transaction_cap, trust_score

app = FastAPI(title="CryptoShield Gravity", version="0.1.0")


class WalletIn(BaseModel):
    age_days: int = Field(ge=0)
    tx_count: int = Field(ge=0)
    successful_ratio: float = Field(ge=0, le=1)
    disputes: int = Field(0, ge=0)
    flagged_counterparties: int = Field(0, ge=0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/score")
def score(w: WalletIn):
    s = trust_score(WalletStats(**w.model_dump()))
    return {"score": s, "cap_usd": transaction_cap(s)}
