"""
05_table2.py
复现论文 Table 2：描述性统计（政策前/后，NJ vs PA）
"""
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("data/processed/ck_analysis.csv")

# ---------- 辅助函数：算 NJ/PA 均值 + t 检验 ----------
def compare(sub, col):
    """返回 (NJ均值, NJ标准误, PA均值, PA标准误, t统计量)"""
    nj = sub[sub["nj"] == 1][col].dropna()
    pa = sub[sub["nj"] == 0][col].dropna()
    t, p = stats.ttest_ind(nj, pa, equal_var=False)
    return (nj.mean(), nj.std(ddof=1)/np.sqrt(len(nj)),
            pa.mean(), pa.std(ddof=1)/np.sqrt(len(pa)), t)

rows = []

# ---------- 1. 门店类型分布（百分比）----------
for code, name in [(1,"a. Burger King"), (2,"b. KFC"),
                   (3,"c. Roy Rogers"), (4,"d. Wendy's")]:
    df["_tmp"] = (df["CHAIN"] == code).astype(float)
    rows.append((name, compare(df, "_tmp")))

df["_tmp"] = df["CO_OWNED"].astype(float)
rows.append(("e. Company-owned", compare(df, "_tmp")))

print("=" * 70)
print("1. 门店类型分布（%）")
print(f"{'Variable':<20}{'NJ':>15}{'PA':>15}{'t':>8}")
for name, (m1, s1, m0, s0, t) in rows:
    print(f"{name:<20}{m1*100:>8.1f}({s1*100:.1f}){m0*100:>8.1f}({s0*100:.1f}){t:>8.1f}")
# ---------- 2. Wave 1 均值 ----------
# 构造需要的变量
df["pct_ft1"]  = df["EMPFT"] / (df["EMPFT"] + df["EMPPT"]) * 100
df["wage425_1"] = (df["WAGE_ST"] == 4.25).astype(float) * 100
df["meal1"]    = df["PSODA"] + df["PFRY"] + df["PENTREE"]
df["bonus1"]   = df["BONUS"].astype(float) * 100

print("\n" + "=" * 70)
print("2. Wave 1 均值（政策前）")
print(f"{'Variable':<25}{'NJ':>15}{'PA':>15}{'t':>8}")
wave1 = [
    ("a. FTE employment",        "emptot1"),
    ("b. Percentage full-time",  "pct_ft1"),
    ("c. Starting wage",         "WAGE_ST"),
    ("d. Wage = $4.25 (%)",      "wage425_1"),
    ("e. Price of full meal",    "meal1"),
    ("f. Hours open (weekday)",  "HRSOPEN"),
    ("g. Recruiting bonus (%)",  "bonus1"),
]
for name, col in wave1:
    m1, s1, m0, s0, t = compare(df, col)
    print(f"{name:<25}{m1:>8.2f}({s1:.2f}){m0:>8.2f}({s0:.2f}){t:>8.1f}")

# ---------- 3. Wave 2 均值 ----------
df["pct_ft2"]   = df["EMPFT2"] / (df["EMPFT2"] + df["EMPPT2"]) * 100
df["wage425_2"] = (df["WAGE_ST2"] == 4.25).astype(float) * 100
df["wage505_2"] = (df["WAGE_ST2"] == 5.05).astype(float) * 100
df["meal2"]     = df["PSODA2"] + df["PFRY2"] + df["PENTREE2"]
df["bonus2"]    = df["SPECIAL2"].astype(float) * 100  # 注意：这里用 SPECIAL2 近似

print("\n" + "=" * 70)
print("3. Wave 2 均值（政策后）")
print(f"{'Variable':<25}{'NJ':>15}{'PA':>15}{'t':>8}")
wave2 = [
    ("a. FTE employment",        "emptot2"),
    ("b. Percentage full-time",  "pct_ft2"),
    ("c. Starting wage",         "WAGE_ST2"),
    ("d. Wage = $4.25 (%)",      "wage425_2"),
    ("e. Wage = $5.05 (%)",      "wage505_2"),
    ("f. Price of full meal",    "meal2"),
    ("g. Hours open (weekday)",  "HRSOPEN2"),
    ("h. Recruiting bonus (%)",  "bonus2"),
]
for name, col in wave2:
    m1, s1, m0, s0, t = compare(df, col)
    print(f"{name:<25}{m1:>8.2f}({s1:.2f}){m0:>8.2f}({s0:.2f}){t:>8.1f}")
# ---------- 保存 Table 2 ----------
table2_rows = []
for name, (m1, s1, m0, s0, t) in rows:
    table2_rows.append({"part": "store_type", "variable": name,
                        "NJ": round(m1*100, 2), "NJ_se": round(s1*100, 2),
                        "PA": round(m0*100, 2), "PA_se": round(s0*100, 2), "t": round(t, 2)})
for name, col in wave1:
    m1, s1, m0, s0, t = compare(df, col)
    table2_rows.append({"part": "wave1", "variable": name,
                        "NJ": round(m1, 3), "NJ_se": round(s1, 3),
                        "PA": round(m0, 3), "PA_se": round(s0, 3), "t": round(t, 2)})
for name, col in wave2:
    m1, s1, m0, s0, t = compare(df, col)
    table2_rows.append({"part": "wave2", "variable": name,
                        "NJ": round(m1, 3), "NJ_se": round(s1, 3),
                        "PA": round(m0, 3), "PA_se": round(s0, 3), "t": round(t, 2)})

pd.DataFrame(table2_rows).to_csv("outputs/tables/table2.csv", index=False)
print("\n已保存到 outputs/tables/table2.csv")