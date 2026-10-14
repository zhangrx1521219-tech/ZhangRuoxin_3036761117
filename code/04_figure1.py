"""
04_figure1.py
复现论文 Figure 1：起薪分布（政策前 vs 政策后，NJ vs PA）
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/ck_analysis.csv")

# ---------- 工资分档：4.25 到 5.55，每 0.10 一档 ----------
bins = np.arange(4.25, 5.55 + 0.05, 0.10)
labels = [f"{b:.2f}" for b in bins[:-1]]

def wage_dist(wage_col):
    """返回 NJ 和 PA 在各工资档的百分比"""
    out = {}
    for state, name in [(1, "NJ"), (0, "PA")]:
        w = df[df["nj"] == state][wage_col].dropna()
        counts = pd.cut(w, bins=bins, labels=labels, right=False).value_counts().sort_index()
        out[name] = counts / counts.sum() * 100
    return out

# ---------- 画两张面板 ----------
fig, axes = plt.subplots(2, 1, figsize=(10, 9))

for ax, col, title in [(axes[0], "WAGE_ST", "February 1992"),
                        (axes[1], "WAGE_ST2", "November 1992")]:
    dist = wage_dist(col)
    x = np.arange(len(labels))
    w = 0.4
    ax.bar(x - w/2, dist["NJ"], width=w, color="black", label="New Jersey")
    ax.bar(x + w/2, dist["PA"], width=w, color="white",
           edgecolor="black", hatch="////", label="Pennsylvania")
    ax.set_title(title, fontsize=14)
    ax.set_ylabel("Percent of Stores")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    ax.set_xlabel("Wage Range")
    ax.legend()

plt.tight_layout()
plt.savefig("outputs/figures/figure1.png", dpi=150)
print("已保存到 outputs/figures/figure1.png")