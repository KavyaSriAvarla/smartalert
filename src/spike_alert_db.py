import sqlite3

conn = sqlite3.connect("data/smartalert.db")

query = """
SELECT t.date, t.merchant, t.amount, t.category, a.avg_amount
FROM transactions t
JOIN (
    SELECT category, AVG(amount) AS avg_amount
    FROM transactions
    GROUP BY category
) a ON t.category = a.category
WHERE t.amount > 2 * a.avg_amount
"""

print("Spike alerts (from database):")
for date, merchant, amount, category, avg_amount in conn.execute(query):
    print(f"ALERT: {category} payment of {amount} at {merchant} on {date} is more than 2x the usual {category} average")

conn.close()