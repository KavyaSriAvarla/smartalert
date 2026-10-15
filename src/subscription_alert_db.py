import sqlite3

conn = sqlite3.connect("data/smartalert.db")

query = """
SELECT merchant, amount, COUNT(*) AS times_paid
FROM transactions
WHERE category = 'Subscription'
GROUP BY merchant, amount
HAVING COUNT(*) >= 2
"""

print("Subscription alerts (from database):")
for merchant, amount, times_paid in conn.execute(query):
    print(f"ALERT: You paid {merchant} {amount} {times_paid} times. Is this a subscription you still need?")

conn.close()