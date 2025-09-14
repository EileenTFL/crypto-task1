## Project Overview
This project implements Challenge Task 1. It queries recent Ethereum transactions for a known public wallet (Ethereum Foundation: 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe), normalizes the data, and outputs:
(a) a directed network graph of the last N transactions,
(b) a CSV of those transactions, and
(c) a plain-English summary (inflow/outflow, counterparties).
Nodes = wallet addresses, Edges = transactions (from → to).

## Installation steps (Windows / VS code)
# from the repo root
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

## Example usage (show how to run)
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -u scripts\task1_wallet_graph.py --n 15
# Outputs created:
1. figs/wallet_graph.png
2. data/processed/txn_sample.csv
3. data/processed/wallet_summary.txt

## Screenshot
![Transaction network graph](figs/wallet_graph.png)
