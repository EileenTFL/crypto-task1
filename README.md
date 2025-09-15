# Crypto Forensics Assessment — Task 1 & Task 2

## Project Overview
**Task 1 (Wallet Graph):** Query recent Ethereum transactions for a known public wallet (Ethereum Foundation: `0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe`), normalize them, and output:
- a **directed network graph** of the last *N* transactions,
- a **CSV** of those transactions,
- a **plain-English summary** (inflow/outflow, counterparties).
Nodes = wallet addresses; Edges = transactions (`from → to`).

**Task 2 (Market Forensics):** Pull recent daily **price & volume** for a token, compute basic anomaly scores (z-scores) for **returns** and **volume**, and output:
- a **price time series** with moving average and anomaly markers,
- a **volume chart** with spikes highlighted,
- a **histogram** of daily returns,
- a short **text report** summarizing flagged days.  
(Uses CoinGecko; automatically falls back to a small fixture so it runs offline.)

---

## Installation (Windows / VS Code)

```powershell
# from the repo root
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Example usage
**Task 1 -- Wallet Graph (Ethereum Foundation)**
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -u scripts\task1_wallet_graph.py --n 15

# Outputs created:
1. figs/wallet_graph.png
2. data/processed/txn_sample.csv
3. data/processed/wallet_summary.txt

**Task 2 -- Market Forensics (CoinGecko, 30 days)**
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -u scripts\task2_market_forensics.py --coin-id bitcoin --days 30 --ma 7 --z 3.0

# Outputs
1. figs/price_ma_bitcoin.png
2. figs/volume_anoms_bitcoin.png
3. figs/returns_hist_bitcoin.png
4. data/processed/ohlcv_bitcoin.csv
5. data/processed/market_report_bitcoin.txt

## Screenshot
![Transaction network graph](figs/wallet_graph.png)
![Price + MA](figs/price_ma_bitcoin.png)
![Volume anomalies](figs/volume_anoms_bitcoin.png)
![Returns histogram](figs/returns_hist_bitcoin.png)
