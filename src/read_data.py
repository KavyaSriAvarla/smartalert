import pandas as pd

df = pd.read_csv("data/transactions.csv")
print(df)
print()
print("Total spent:", df["amount"].sum())
print()
print(df.groupby("category")["amount"].sum())

# Biggest transaction
biggest = df.loc[df["amount"].idxmax()]
print("\nBiggest transaction:")
print(biggest)

# Average spend per category
avg_per_category = df.groupby("category")["amount"].mean()
print("\nAverage spend per category:")
print(avg_per_category)