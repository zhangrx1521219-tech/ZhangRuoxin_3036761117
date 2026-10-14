import pandas as pd

df = pd.read_csv("data/raw/public.csv")

print("总行数:", len(df))
print()
print("各州数量（1=NJ, 0=PA）:")
print(df["STATE"].value_counts())
print()
print("STATUS2 分布:")
print(df["STATUS2"].value_counts(dropna=False).sort_index())