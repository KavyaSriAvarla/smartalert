import sqlite3
import pandas as pd

conn = sqlite3.connect("data/smartalert.db")

# 1. Save budgets.csv into the database as a table
budgets = pd.read_csv("data/budgets.csv")
budgets.to_sql("budgets", conn, if_exists="replace", index=False)


# 2. Match each category's budget with its spend in the latest month
query = """
SELECT b.category, b.budget, SUM(t.amount) AS spent
FROM budgets b
JOIN transactions t ON t.category = b.category
WHERE strftime('%Y-%m', t.date) = (
    SELECT MAX(strftime('%Y-%m', date)) FROM transactions
)
GROUP BY b.category, b.budget
"""

# 3. Print alerts
print("Budget alerts (from database):")
for category, budget, spent in conn.execute(query):
    if spent > budget:
        print(f"ALERT: {category} budget is {budget}, you spent {spent}")
    else:
        print(f"OK: {category} spent {spent} of {budget}")

conn.close()