# CryptoShield Gravity (CVG)

Trust-scoring service that caps how much a wallet can send per transaction based on its on-chain reputation. Built to make P2P crypto scams less profitable: a brand-new wallet can only move small amounts, and limits grow as it builds a clean history.

## How it works
`app/scoring.py` turns wallet age, activity, completed-trade ratio, disputes and flagged counterparties into a 0-100 score. Score bands map to a per-transaction cap in USD, similar to how credit limits follow credit scores.

## API
```
POST /score   {"age_days":500,"tx_count":200,"successful_ratio":0.97}
  -> {"score": 78.4, "cap_usd": 1000.0}
GET  /health
```

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -q
```

## Planned
SIWE (EIP-4361) and WebAuthn login, SHA-256 Merkle ledger for score history, Hyperledger Fabric integration, PostgreSQL storage, React + D3 dashboard.

Current state: scoring core and API. The weights are a first draft and need calibration against real labelled data.
