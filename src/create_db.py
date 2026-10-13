import sqlite3
import pandas as pd

# 1. Read the CSV
df = pd.read_csv("data/transactions_large.csv")

# 2. Connect to a database (this creates the file if it doesn't exist)
conn = sqlite3.connect("data/smartalert.db")

# 3. Save the data as a table called "transactions"
df.to_sql("transactions", conn, if_exists="replace", index=False)

# 4. Check how many rows were saved
count = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
print("Rows saved:", count)

conn.close()