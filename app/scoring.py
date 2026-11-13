"""Trust scoring for wallets and the transaction cap derived from it.

Idea borrowed from credit scoring: a wallet earns a score from observable
on-chain behaviour, and the score decides how much it may send per transaction.
"""
from dataclasses import dataclass
import math


@dataclass
class WalletStats:
    age_days: int
    tx_count: int
    successful_ratio: float   # 0..1 of completed, undisputed trades
    disputes: int
    flagged_counterparties: int


def trust_score(w: WalletStats) -> float:
    """Return a score in [0, 100]."""
    age = min(w.age_days / 365, 1.0) * 25
    volume = min(math.log1p(w.tx_count) / math.log1p(500), 1.0) * 25
    quality = max(0.0, min(w.successful_ratio, 1.0)) * 40
    penalty = w.disputes * 8 + w.flagged_counterparties * 6
    return round(max(0.0, min(100.0, age + volume + quality + 10 - penalty)), 2)


TIERS = [(80, 5000.0), (60, 1000.0), (40, 250.0), (20, 50.0), (0, 10.0)]


def transaction_cap(score: float) -> float:
    """Max single-transaction amount (USD) allowed at a given score."""
    for floor, cap in TIERS:
        if score >= floor:
            return cap
    return TIERS[-1][1]
