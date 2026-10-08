import pandas as pd

df = pd.read_csv("data/transactions.csv")
print(df)
print()
print("Total spent:", df["amount"].sum())
print()
print(df.groupby("category")["amount"].sum())