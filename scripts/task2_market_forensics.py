# scripts/task2_market_forensics.py
import argparse
from pathlib import Path
from src.cg_client import fetch_ohlcv
from src.analytics import AnomalyConfig, compute_indicators, make_report
from src.plotting import plot_price_ma, plot_volume_anoms, plot_returns_hist

def main():
    p = argparse.ArgumentParser(description="Task 2: Market Forensics (CoinGecko)")
    p.add_argument("--coin-id", default="bitcoin", help="CoinGecko coin id (e.g., bitcoin, ethereum, dogecoin)")
    p.add_argument("--days", type=int, default=30, help="Days of daily history")
    p.add_argument("--ma", type=int, default=7, help="Moving-average window (days)")
    p.add_argument("--z", type=float, default=3.0, help="Z-score threshold for anomalies")
    args = p.parse_args()

    df = fetch_ohlcv(args.coin_id, args.days)
    cfg = AnomalyConfig(ma_window=args.ma, z_thresh=args.z)
    feat = compute_indicators(df, cfg)

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    csv_path = f"data/processed/ohlcv_{args.coin_id}.csv"
    feat.to_csv(csv_path, index=False)

    plot_price_ma(feat, f"figs/price_ma_{args.coin_id}.png", f"{args.coin_id}: price + {args.ma}D MA (|z|>{args.z})")
    plot_volume_anoms(feat, f"figs/volume_anoms_{args.coin_id}.png", f"{args.coin_id}: volume anomalies (|z|>{args.z})")
    plot_returns_hist(feat, f"figs/returns_hist_{args.coin_id}.png", f"{args.coin_id}: daily returns histogram")

    report = make_report(feat, args.coin_id, cfg)
    Path(f"data/processed/market_report_{args.coin_id}.txt").write_text(report, encoding="utf-8")
    print(report)

if __name__ == "__main__":
    main()
