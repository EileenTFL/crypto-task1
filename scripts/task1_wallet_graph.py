import argparse
from pathlib import Path
from src.etherscan_client import EtherscanClient
from src.normalize import normalize_txlist
from src.graphing import build_digraph, draw_graph, compute_summary

DEFAULT_ADDR = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe"  # Ethereum Foundation

def main():
    p = argparse.ArgumentParser(description="Task 1: Wallet transaction graph")
    p.add_argument("--address", default=DEFAULT_ADDR)
    p.add_argument("--n", type=int, default=15)
    p.add_argument("--out", default="figs/wallet_graph.png")
    args = p.parse_args()

    client = EtherscanClient()
    rows = client.txlist(args.address, sort="desc", page=1, offset=max(100, args.n))
    df = normalize_txlist(rows)
    if df.empty:
        raise SystemExit("No transactions available for this address.")
    sample = df.sort_values("time", ascending=False).head(args.n).copy()

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    sample.to_csv("data/processed/txn_sample.csv", index=False)

    g = build_digraph(sample, args.address)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    draw_graph(g, args.address, args.out)

    summary = compute_summary(sample, args.address)
    Path("data/processed/wallet_summary.txt").write_text(summary)
    print(summary)

if __name__ == "__main__":
    main()
