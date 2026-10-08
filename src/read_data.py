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

# Budget alerts
budgets = pd.read_csv("data/budgets.csv")
spend = df.groupby("category")["amount"].sum()

print("\nBudget alerts:")
for _, row in budgets.iterrows():
    category = row["category"]
    limit = row["budget"]
    spent = spend.get(category, 0)
    if spent > limit:
        print(f"ALERT: {category} budget is {limit}, you spent {spent}")
    else:
        print(f"OK: {category} spent {spent} of {limit}")