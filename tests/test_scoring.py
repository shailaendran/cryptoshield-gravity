from fastapi.testclient import TestClient

from app.main import app
from app.scoring import WalletStats, transaction_cap, trust_score

client = TestClient(app)


def test_new_wallet_low_cap():
    s = trust_score(WalletStats(0, 0, 0.0, 0, 0))
    assert transaction_cap(s) == 10.0


def test_established_wallet_high_cap():
    s = trust_score(WalletStats(800, 600, 0.99, 0, 0))
    assert s >= 80 and transaction_cap(s) == 5000.0


def test_disputes_reduce_score():
    good = trust_score(WalletStats(400, 100, 0.95, 0, 0))
    bad = trust_score(WalletStats(400, 100, 0.95, 4, 2))
    assert bad < good


def test_score_bounded():
    assert 0 <= trust_score(WalletStats(9999, 99999, 1.0, 0, 0)) <= 100
    assert trust_score(WalletStats(0, 0, 0.0, 50, 50)) == 0


def test_api_score():
    r = client.post("/score", json={"age_days": 500, "tx_count": 200, "successful_ratio": 0.97})
    assert r.status_code == 200 and "cap_usd" in r.json()


def test_api_rejects_bad_ratio():
    assert client.post("/score", json={"age_days": 1, "tx_count": 1, "successful_ratio": 2}).status_code == 422
