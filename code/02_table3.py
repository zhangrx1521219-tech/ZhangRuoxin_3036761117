"""
02_table3.py
完整复现论文 Table 3：8 列 x 5 行
"""
import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/ck_analysis.csv")

# ---------- 给 NJ 店打"工资组"标签 ----------
def wage_group(row):
    if row["nj"] == 0:
        return "PA"
    if row["WAGE_ST"] == 4.25:
        return "NJ_low"
    if 4.26 <= row["WAGE_ST"] <= 4.99:
        return "NJ_mid"
    if row["WAGE_ST"] >= 5.00:
        return "NJ_high"
    return "NJ_other"

df["wgroup"] = df.apply(wage_group, axis=1)

# ---------- 计算某一组的 5 行 ----------
def means(sub):
    r1 = sub["emptot1"].mean()
    r2 = sub["emptot2"].mean()
    r3 = r2 - r1
    bal = sub.dropna(subset=["emptot1", "emptot2"])
    r4 = bal["emptotd"].mean()
    s5 = sub.copy()
    s5.loc[s5["STATUS2"].isin([2, 4, 5]), "emptot2"] = 0
    s5["d5"] = s5["emptot2"] - s5["emptot1"]
    r5 = s5.dropna(subset=["emptot1", "emptot2"])["d5"].mean()
    return r1, r2, r3, r4, r5

# ---------- 各组（注意 NJ 用 nj==1 单独筛）----------
cols = {}
cols["PA"]     = means(df[df["nj"] == 0])
cols["NJ"]     = means(df[df["nj"] == 1])          # ← 修复点
cols["NJ_low"] = means(df[df["wgroup"] == "NJ_low"])
cols["NJ_mid"] = means(df[df["wgroup"] == "NJ_mid"])
cols["NJ_high"]= means(df[df["wgroup"] == "NJ_high"])

# ---------- 组装 8 列 ----------
out = pd.DataFrame(index=["1. FTE before", "2. FTE after",
                          "3. Change", "4. Change (balanced)",
                          "5. Change (temp=0)"])
out["(i) PA"]      = cols["PA"]
out["(ii) NJ"]     = cols["NJ"]
out["(iii) NJ-PA"] = out["(ii) NJ"] - out["(i) PA"]
out["(iv) 4.25"]       = cols["NJ_low"]
out["(v) 4.26-4.99"]   = cols["NJ_mid"]
out["(vi) >=5.00"]     = cols["NJ_high"]
out["(vii) low-high"]  = out["(iv) 4.25"] - out["(vi) >=5.00"]
out["(viii) mid-high"] = out["(v) 4.26-4.99"] - out["(vi) >=5.00"]

print(out.round(2).to_string())
out.round(4).to_csv("outputs/tables/table3.csv")
print("\n已保存到 outputs/tables/table3.csv")
