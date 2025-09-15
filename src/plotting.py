# src/plotting.py
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def plot_price_ma(df: pd.DataFrame, out_path: str, title: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["price"], label="price")
    plt.plot(df["time"], df["ma"], label="moving avg")
    an = df[df["anomaly_ret"]]
    if not an.empty:
        plt.scatter(an["time"], an["price"], s=50, marker="o", label="return anomaly")
        for _, r in an.iterrows():
            plt.annotate("⚠", (r["time"], r["price"]), xytext=(0, 8), textcoords="offset points", ha="center")
    plt.title(title); plt.xlabel("time (UTC)"); plt.ylabel("price (USD)")
    plt.legend(); plt.tight_layout(); plt.savefig(out_path, dpi=200); plt.close()

def plot_volume_anoms(df: pd.DataFrame, out_path: str, title: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 4))
    plt.bar(df["time"], df["volume"], width=0.8, align="center")
    an = df[df["anomaly_vol"]]
    if not an.empty:
        plt.scatter(an["time"], an["volume"], s=40, marker="x")
        for _, r in an.iterrows():
            plt.annotate("spike", (r["time"], r["volume"]), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8)
    plt.title(title); plt.xlabel("time (UTC)"); plt.ylabel("volume (USD)")
    plt.tight_layout(); plt.savefig(out_path, dpi=200); plt.close()

def plot_returns_hist(df: pd.DataFrame, out_path: str, title: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5))
    df["ret"].dropna().hist(bins=30)
    plt.title(title); plt.xlabel("daily return"); plt.ylabel("frequency")
    plt.tight_layout(); plt.savefig(out_path, dpi=200); plt.close()
