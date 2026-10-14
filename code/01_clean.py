"""
01_clean.py
Card & Krueger (1994) 复现 —— 数据清洗
构造 FTE、处理关店、生成分析数据集
"""
import pandas as pd

# ---------- 1. 读入原始数据 ----------
df = pd.read_csv("data/raw/public.csv")
print(f"原始数据：{len(df)} 行")

# ---------- 2. 构造 FTE ----------
# 论文定义：FTE = 全职 + 经理 + 0.5 × 兼职
df["emptot1"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]      # 政策前
df["emptot2"] = df["EMPFT2"] + df["NMGRS2"] + 0.5 * df["EMPPT2"]   # 政策后

# ---------- 3. 处理关店（论文 Table 1 & 第4页）----------
# STATUS2: 0=拒访, 1=正常, 2=装修, 3=永久关闭, 4=修路, 5=火灾
# 永久关闭 -> 第二波 FTE 记 0
df.loc[df["STATUS2"] == 3, "emptot2"] = 0
# 拒访/装修/修路/火灾 -> 第二波 FTE 记缺失
df.loc[df["STATUS2"].isin([0, 2, 4, 5]), "emptot2"] = float("nan")

# ---------- 4. 生成分析变量 ----------
df["emptotd"] = df["emptot2"] - df["emptot1"]   # 就业变化（因变量）
df["nj"] = df["STATE"]                            # 1=NJ(处理组), 0=PA(对照组)

# ---------- 5. 检查 ----------
print("\n--- 清洗后关键变量 ---")
print("emptot1 非缺失:", df["emptot1"].notna().sum())
print("emptot2 非缺失:", df["emptot2"].notna().sum())
print("emptotd 非缺失:", df["emptotd"].notna().sum())
print("\n按州分组的平均 FTE（政策前）:")
print(df.groupby("nj")["emptot1"].mean().round(2))

# ---------- 6. 保存 ----------
df.to_csv("data/processed/ck_analysis.csv", index=False)
print("\n已保存到 data/processed/ck_analysis.csv")