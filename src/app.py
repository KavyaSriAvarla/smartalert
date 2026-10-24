import sqlite3
import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="SmartAlert", page_icon="💸")
st.title("SmartAlert 💸")

# ---------- Load data from the database ----------
conn = sqlite3.connect("data/smartalert.db")
df = pd.read_sql("SELECT * FROM transactions", conn)
budgets = pd.read_sql("SELECT * FROM budgets", conn)
conn.close()

df["month"] = df["date"].str[:7]
latest = df["month"].max()
month_spend = df[df["month"] == latest].groupby("category")["amount"].sum()

# ---------- Overview ----------
st.metric("Total spent", int(df["amount"].sum()))

st.subheader("Spend per category")
spend = df.groupby("category")["amount"].sum().reset_index()
st.bar_chart(spend, x="category", y="amount")

# ---------- Alerts ----------
st.header("🚨 Alerts")

st.subheader(f"Budget alerts ({latest})")
for _, row in budgets.iterrows():
    spent = int(month_spend.get(row["category"], 0))
    if spent > row["budget"]:
        st.error(f"{row['category']}: budget is {row['budget']}, you spent {spent}")
    else:
        st.success(f"{row['category']}: spent {spent} of {row['budget']}")

st.subheader("Spike alerts")
df["category_avg"] = df.groupby("category")["amount"].transform("mean")
spikes = df[df["amount"] > 2 * df["category_avg"]]
if spikes.empty:
    st.info("No spikes found.")
for _, r in spikes.iterrows():
    st.warning(f"{r['category']} payment of {r['amount']} at {r['merchant']} on {r['date']} is more than 2x the usual average")

st.subheader("Subscription alerts")
subs = df[df["category"] == "Subscription"].groupby(["merchant", "amount"]).size().reset_index(name="times_paid")
subs = subs[subs["times_paid"] >= 2]
if subs.empty:
    st.info("No repeated subscriptions found.")
for _, r in subs.iterrows():
    st.warning(f"You paid {r['merchant']} {r['amount']} {r['times_paid']} times. Is this a subscription you still need?")

st.subheader("🤖 AI anomaly detection (Isolation Forest)")
df["ratio"] = df["amount"] / df["category_avg"]
model = IsolationForest(contamination=0.02, random_state=42)
model.fit(df[["amount", "ratio"]])
df["score"] = model.decision_function(df[["amount", "ratio"]])
unusual = df[df["score"] < -0.1].sort_values("score")
st.dataframe(unusual[["date", "merchant", "amount", "category", "score"]])

# ---------- Latest transactions ----------
st.subheader("Latest transactions")
st.dataframe(df[["date", "merchant", "amount", "category"]].tail(10))