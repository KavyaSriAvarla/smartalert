import sqlite3

conn = sqlite3.connect("data/smartalert.db")

query = """
SELECT category, SUM(amount) AS total_spend
FROM transactions
GROUP BY category
ORDER BY total_spend DESC
"""

for row in conn.execute(query):
    print(row)

conn.close()