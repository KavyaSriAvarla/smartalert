import sqlite3

conn = sqlite3.connect("data/smartalert.db")

query = """
SELECT category, SUM(amount) AS month_spend
FROM transactions
WHERE strftime('%Y-%m', date) = (
    SELECT MAX(strftime('%Y-%m', date)) FROM transactions
)
GROUP BY category
"""

for row in conn.execute(query):
    print(row)

conn.close()