"""
06_extension.py
Extension: 最低工资就业效应的异质性分析
① 受约束程度  ② 连锁品牌  ③ 所有权结构
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy import stats

df = pd.read_csv("data/processed/ck_analysis.csv")

# ---------- 构造 GAP ----------
def make_gap(row):
    if row["nj"] == 0:
        return 0.0
    if row["WAGE_ST"] >= 5.05:
        return 0.0
    if pd.isna(row["WAGE_ST"]):
        return np.nan
    return (5.05 - row["WAGE_ST"]) / row["WAGE_ST"]

df["gap"] = df.apply(make_gap, axis=1)
df["chain_kfc"]   = (df["CHAIN"] == 2).astype(int)
df["chain_roy"]   = (df["CHAIN"] == 3).astype(int)
df["chain_wendy"] = (df["CHAIN"] == 4).astype(int)

# ---------- 统一样本（同 Table 4，365家）----------
s = df.dropna(subset=["emptot1", "emptot2", "WAGE_ST"]).copy()
print(f"统一样本量: {len(s)}\n")

results = []

# ============================================================
# ① 受约束程度：三组 + 组间检验
# ============================================================
print("=" * 72)
print("① 按受约束程度分组（NJ 内部，就业变化 emptotd）")
print("=" * 72)
nj = s[s["nj"] == 1].copy()
nj["group"] = pd.cut(nj["WAGE_ST"], bins=[4.24, 4.26, 4.99, 100],
                     labels=["low ($4.25)", "mid", "high (>=5.00)"])

print(f"{'组':<18}{'N':>5}{'均值':>10}{'标准误':>10}{'t (vs high)':>14}")
high = nj[nj["group"] == "high (>=5.00)"]["emptotd"]
for g in ["low ($4.25)", "mid", "high (>=5.00)"]:
    vals = nj[nj["group"] == g]["emptotd"]
    se = vals.std(ddof=1) / np.sqrt(len(vals))
    t, p = stats.ttest_ind(vals, high, equal_var=False)
    print(f"{g:<18}{len(vals):>5}{vals.mean():>10.3f}{se:>10.3f}{t:>10.2f} (p={p:.3f})")
    results.append({"analysis": "binding", "group": g, "N": len(vals),
                    "mean": round(vals.mean(), 3), "se": round(se, 3), "t_vs_high": round(t, 2)})

# ============================================================
# ② 连锁品牌：GAP 回归（同一控制变量集）
# ============================================================
print("\n" + "=" * 72)
print("② 按连锁品牌：回归 emptotd ~ gap + CO_OWNED")
print("=" * 72)
print(f"{'品牌':<16}{'N':>5}{'GAP系数':>12}{'SE':>10}{'p值':>10}")
for chain, name in [(1,"Burger King"), (2,"KFC"), (3,"Roy Rogers"), (4,"Wendy's")]:
    sub = s[s["CHAIN"] == chain]
    m = smf.ols("emptotd ~ gap + CO_OWNED", data=sub).fit()
    print(f"{name:<16}{len(sub):>5}{m.params['gap']:>12.2f}{m.bse['gap']:>10.2f}{m.pvalues['gap']:>10.3f}")
    results.append({"analysis": "chain", "group": name, "N": len(sub),
                    "gap_coef": round(m.params['gap'], 3),
                    "se": round(m.bse['gap'], 3), "p": round(m.pvalues['gap'], 3)})

# ============================================================
# ③ 所有权结构：GAP 回归
# ============================================================
print("\n" + "=" * 72)
print("③ 按所有权结构：回归 emptotd ~ gap + chain dummies")
print("=" * 72)
print(f"{'类型':<18}{'N':>5}{'GAP系数':>12}{'SE':>10}{'p值':>10}")
for own, name in [(1,"Company-owned"), (0,"Franchise")]:
    sub = s[s["CO_OWNED"] == own]
    m = smf.ols("emptotd ~ gap + chain_kfc + chain_roy + chain_wendy", data=sub).fit()
    print(f"{name:<18}{len(sub):>5}{m.params['gap']:>12.2f}{m.bse['gap']:>10.2f}{m.pvalues['gap']:>10.3f}")
    results.append({"analysis": "ownership", "group": name, "N": len(sub),
                    "gap_coef": round(m.params['gap'], 3),
                    "se": round(m.bse['gap'], 3), "p": round(m.pvalues['gap'], 3)})

# ---------- 保存 ----------
pd.DataFrame(results).to_csv("outputs/tables/extension.csv", index=False)
print("\n已保存到 outputs/tables/extension.csv")