"""
03_table4.py
复现论文 Table 4：就业变化的回归模型
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

df = pd.read_csv("data/processed/ck_analysis.csv")

# ---------- 构造 GAP 变量 ----------
def make_gap(row):
    if row["nj"] == 0:                     # PA
        return 0.0
    if row["WAGE_ST"] >= 5.05:             # NJ 高工资
        return 0.0
    if pd.isna(row["WAGE_ST"]):
        return np.nan
    return (5.05 - row["WAGE_ST"]) / row["WAGE_ST"]

df["gap"] = df.apply(make_gap, axis=1)

# ---------- chain 虚拟变量 ----------
df["chain_kfc"]   = (df["CHAIN"] == 2).astype(int)
df["chain_roy"]   = (df["CHAIN"] == 3).astype(int)
df["chain_wendy"] = (df["CHAIN"] == 4).astype(int)

# ---------- region 虚拟变量 ----------
# NJ: SOUTHJ / CENTRALJ / NORTHJ；PA: PA1 / PA2
df["reg_nj_south"]   = df["SOUTHJ"]
df["reg_nj_central"] = df["CENTRALJ"]
df["reg_pa1"]        = df["PA1"]
df["reg_pa2"]        = df["PA2"]

# ---------- 限制样本：两波就业和起薪都齐全的店 ----------
s = df.dropna(subset=["emptot1", "emptot2", "WAGE_ST"]).copy()
print(f"样本量（论文 357，我们 365）: {len(s)}")
print(f"样本量（应为 357）: {len(s)}")
print(f"因变量均值（应为 -0.237）: {s['emptotd'].mean():.3f}")
print(f"因变量标准差（应为 8.825）: {s['emptotd'].std(ddof=1):.3f}")
print()

# ---------- 5 个模型 ----------
m1 = smf.ols("emptotd ~ nj", data=s).fit()
m2 = smf.ols("emptotd ~ nj + chain_kfc + chain_roy + chain_wendy + CO_OWNED", data=s).fit()
m3 = smf.ols("emptotd ~ gap", data=s).fit()
m4 = smf.ols("emptotd ~ gap + chain_kfc + chain_roy + chain_wendy + CO_OWNED", data=s).fit()
m5 = smf.ols("emptotd ~ gap + chain_kfc + chain_roy + chain_wendy + CO_OWNED "
             "+ reg_nj_south + reg_nj_central + reg_pa1 + reg_pa2", data=s).fit()

models = {"(i)": m1, "(ii)": m2, "(iii)": m3, "(iv)": m4, "(v)": m5}

# ---------- 整理输出 ----------
print(f"{'变量':<25}", "".join(f"{k:>12}" for k in models))
for var in ["nj", "gap"]:
    row = f"{var:<25}"
    for k, m in models.items():
        if var in m.params:
            row += f"{m.params[var]:>12.2f}"
        else:
            row += f"{'—':>12}"
    print(row)

print("\n标准误（括号里是论文值）:")
for var in ["nj", "gap"]:
    for k, m in models.items():
        if var in m.params:
            print(f"  {k} {var}: {m.bse[var]:.2f}")

print(f"\n回归标准误:")
for k, m in models.items():
    print(f"  {k}: {np.sqrt(m.mse_resid):.2f}")
# ---------- 保存 Table 4 结果 ----------
rows = []
for k, m in models.items():
    for var in ["nj", "gap"]:
        if var in m.params:
            rows.append({
                "model": k,
                "variable": var,
                "coef": round(m.params[var], 4),
                "se": round(m.bse[var], 4),
            })
# 加上样本信息
rows.append({"model": "sample", "variable": "N", "coef": len(s), "se": None})
rows.append({"model": "sample", "variable": "mean_dep", "coef": round(s["emptotd"].mean(), 4), "se": None})
rows.append({"model": "sample", "variable": "sd_dep", "coef": round(s["emptotd"].std(ddof=1), 4), "se": None})

pd.DataFrame(rows).to_csv("outputs/tables/table4.csv", index=False)
print("\n已保存到 outputs/tables/table4.csv")