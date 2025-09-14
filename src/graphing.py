import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def build_digraph(df: pd.DataFrame, focus_addr: str) -> nx.DiGraph:
    g = nx.DiGraph()
    focus = focus_addr.lower()
    for _, r in df.iterrows():
        u = r["from"]; v = r["to"]
        if pd.isna(u) or pd.isna(v):
            continue
        g.add_node(u)
        g.add_node(v)
        if g.has_edge(u, v):
            g[u][v]["value_eth"] += float(r["value_eth"])
            g[u][v]["count"] += 1
        else:
            g.add_edge(u, v, value_eth=float(r["value_eth"]), count=1)
    if focus not in g:
        g.add_node(focus)
    g.nodes[focus]["focus"] = True
    return g

def draw_graph(g: nx.DiGraph, focus_addr: str, out_path: str) -> None:
    focus = focus_addr.lower()
    pos = nx.spring_layout(g, k=0.8, seed=42)
    plt.figure(figsize=(10,7))
    node_sizes = [600 if n==focus else 200 for n in g.nodes()]
    nx.draw_networkx_nodes(g, pos, node_size=node_sizes)
    widths = [max(1.0, 2.5 * (g[u][v]['value_eth']**0.5)) for u,v in g.edges()]
    nx.draw_networkx_edges(g, pos, width=widths, arrows=True, arrowstyle='->')
    labels = {n:(n[:6]+'…'+n[-4:]) for n in g.nodes()}
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=8)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

def compute_summary(df: pd.DataFrame, focus_addr: str) -> str:
    f = focus_addr.lower()
    recent = df.copy()
    inflow = recent.loc[recent["to"]==f, "value_eth"].sum()
    outflow = recent.loc[recent["from"]==f, "value_eth"].sum()
    net = inflow - outflow
    unique_in = recent.loc[recent["to"]==f, "from"].nunique()
    unique_out = recent.loc[recent["from"]==f, "to"].nunique()
    last_time = recent["time"].max()
    return (
        f"Summary for {f}\n"
        f"Transactions considered: {len(recent)} (most recent)\n"
        f"Last activity (UTC): {last_time}\n"
        f"Inflow ETH: {inflow:.6f}\n"
        f"Outflow ETH: {outflow:.6f}\n"
        f"Net flow ETH: {net:.6f}\n"
        f"Unique counterparties (in/out): {unique_in}/{unique_out}\n"
    )
