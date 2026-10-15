import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Read transactions from the database
conn = sqlite3.connect("data/smartalert.db")
df = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

# 2. Make a helpful feature: how big is this payment compared to its category average?
df["category_avg"] = df.groupby("category")["amount"].transform("mean")
df["ratio"] = df["amount"] / df["category_avg"]

# 3. Train the model (contamination = about 2% of payments are unusual)
model = IsolationForest(contamination=0.02, random_state=42)
df["flag"] = model.fit_predict(df[["amount", "ratio"]])

# 4. Score how unusual each payment is (lower score = more unusual)
df["score"] = model.decision_function(df[["amount", "ratio"]])

unusual = df[df["score"] < -0.1].sort_values("score")
print("Unusual transactions found by Isolation Forest:")
print(unusual[["date", "merchant", "amount", "category", "score"]])