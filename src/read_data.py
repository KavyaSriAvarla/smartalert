import pandas as pd

df = pd.read_csv("data/transactions_large.csv")
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
df["date"] = pd.to_datetime(df["date"])
latest_month = df["date"].dt.to_period("M").max()
this_month = df[df["date"].dt.to_period("M") == latest_month]
spend = this_month.groupby("category")["amount"].sum()

print("\nBudget alerts:")
for _, row in budgets.iterrows():
    category = row["category"]
    limit = row["budget"]
    spent = spend.get(category, 0)
    if spent > limit:
        print(f"ALERT: {category} budget is {limit}, you spent {spent}")
    else:
        print(f"OK: {category} spent {spent} of {limit}")
# Spike alert
category_avg = df.groupby("category")["amount"].transform("mean")
spikes = df[df["amount"] > 2 * category_avg]

print("\nSpike alerts:")
if spikes.empty:
    print("No unusual spikes found.")
else:
    for _, row in spikes.iterrows():
        print(f"ALERT: {row['category']} payment of {row['amount']} is more than 2x the usual {row['category']} average")

# ---------- Subscription alerts ----------
subs = df[df["category"] == "Subscription"]
counts = subs.groupby(["merchant", "amount"]).size()
recurring = counts[counts >= 2]

print("\nSubscription alerts:")
if recurring.empty:
    print("No recurring payments found.")
else:
    for (merchant, amount), times in recurring.items():
        print(f"ALERT: You paid {merchant} {amount} {times} times. Is this a subscription you still need?")
