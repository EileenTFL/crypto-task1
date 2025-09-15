# src/analytics.py
from dataclasses import dataclass
import pandas as pd

@dataclass
class AnomalyConfig:
    ma_window: int = 7
    z_thresh: float = 3.0  # flag if |z| >= this

def compute_indicators(df: pd.DataFrame, cfg: AnomalyConfig) -> pd.DataFrame:
    out = df.copy()
    out["ret"] = out["price"].pct_change()

    # Rolling stats (min_periods keeps early rows)
    out["ma"] = out["price"].rolling(cfg.ma_window, min_periods=1).mean()
    out["vol_ma"] = out["volume"].rolling(cfg.ma_window, min_periods=1).mean()
    out["ret_std"] = out["ret"].rolling(cfg.ma_window, min_periods=2).std().fillna(0.0)
    out["vol_std"] = out["volume"].rolling(cfg.ma_window, min_periods=2).std().fillna(0.0)

    # Z-scores
    out["ret_z"] = out["ret"].where(out["ret_std"] > 0, 0) / out["ret_std"].where(out["ret_std"] > 0, 1)
    out["vol_z"] = (out["volume"] - out["vol_ma"]).where(out["vol_std"] > 0, 0) / out["vol_std"].where(out["vol_std"] > 0, 1)

    # Flags
    out["anomaly_ret"] = out["ret_z"].abs() >= cfg.z_thresh
    out["anomaly_vol"] = out["vol_z"].abs() >= cfg.z_thresh
    out["anomaly_any"] = out["anomaly_ret"] | out["anomaly_vol"]
    return out

def make_report(df: pd.DataFrame, coin_id: str, cfg: AnomalyConfig) -> str:
    n = len(df)
    n_ret = int(df["anomaly_ret"].sum())
    n_vol = int(df["anomaly_vol"].sum())
    n_any = int(df["anomaly_any"].sum())
    last = df["time"].max()

    tops = df.assign(abs_ret_z=df["ret_z"].abs()).nlargest(3, "abs_ret_z")[["time", "ret", "ret_z"]]
    lines = [
        f"Market Forensics Report — {coin_id}",
        f"Window: {n} days; MA={cfg.ma_window}; z-threshold={cfg.z_thresh}",
        f"Last data point (UTC): {last}",
        f"Anomalies — returns: {n_ret}, volume: {n_vol}, any: {n_any}",
        "",
        "Top return spikes (time, return, z):",
    ]
    for _, r in tops.iterrows():
        lines.append(f"- {r['time']} | ret={r['ret']:.4f} | z={r['ret_z']:.2f}")
    lines += [
        "",
        "Heuristics:",
        "- Large return spike with large volume spike may indicate pump/dump or cascade.",
        "- Large volume spike with small price move may indicate wash trading/churn.",
        "- Clusters of anomalies across adjacent days may indicate sustained manipulation risk.",
    ]
    return "\n".join(lines)
