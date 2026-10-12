import random
import pandas as pd
from datetime import date, timedelta

random.seed(42)

# Normal spending: (merchant, category, min amount, max amount)
normal = [
    ("Swiggy", "Food", 150, 600),
    ("Zomato", "Food", 150, 700),
    ("Uber", "Travel", 80, 400),
    ("Amazon", "Shopping", 300, 3000),
    ("Myntra", "Shopping", 400, 2500),
]

rows = []
start = date(2026, 7, 1)

# 92 days = July, August and September
for day in range(92):
    current = start + timedelta(days=day)

    # 1 to 4 random purchases each day
    for i in range(random.randint(1, 4)):
        merchant, category, low, high = random.choice(normal)
        amount = random.randint(low, high)
        rows.append([current, merchant, amount, category])

# Monthly subscription and bill
for month in [7, 8, 9]:
    rows.append([date(2026, month, 5), "Netflix", 299, "Subscription"])
    rows.append([date(2026, month, 10), "Electricity Bill", 1500, "Bills"])

# Two unusual big spends (spikes)
rows.append([date(2026, 8, 14), "Swiggy", 4500, "Food"])
rows.append([date(2026, 9, 2), "Amazon", 9500, "Shopping"])

# Put everything into a table, sorted by date
df = pd.DataFrame(rows, columns=["date", "merchant", "amount", "category"])
df = df.sort_values("date")

# Save to a new file (your old 10-row file stays safe)
df.to_csv("data/transactions_large.csv", index=False)
print("Done! Rows created:", len(df))