import sqlite3
import pandas as pd
import streamlit as st

st.title("SmartAlert 💸")

# Read transactions from the database
conn = sqlite3.connect("data/smartalert.db")
df = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

st.metric("Total spent", int(df["amount"].sum()))

st.subheader("Spend per category")
spend = df.groupby("category")["amount"].sum().reset_index()
st.bar_chart(spend, x="category", y="amount")

st.subheader("Latest transactions")
st.dataframe(df.tail(10))