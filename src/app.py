import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="SmartAlert", page_icon="💸", layout="wide")

GOLD, TEAL, RED, VIOLET = "#F5B841", "#1ED3B0", "#FF5C7A", "#7C83FF"
PALETTE = [GOLD, TEAL, VIOLET, RED, "#C084FC"]

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
html, body, .stApp { font-family: 'Poppins', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(124, 58, 237, 0.35) 0%, transparent 42%),
        radial-gradient(circle at 88% 18%, rgba(30, 211, 176, 0.22) 0%, transparent 40%),
        linear-gradient(180deg, #0b0d1a 0%, #140a24 100%);
    background-attachment: fixed;
}
section[data-testid="stSidebar"] {
    background: rgba(14, 17, 34, 0.75);
    backdrop-filter: blur(12px);
    border-right: 1px solid #2B3345;
}

.hero {
    padding: 28px 32px; border-radius: 20px; margin-bottom: 18px;
    background: linear-gradient(120deg, rgba(27, 31, 58, 0.85) 0%, rgba(42, 31, 61, 0.85) 50%, rgba(61, 42, 31, 0.85) 100%);
    border: 1px solid #2B3345;
    box-shadow: 0 8px 40px rgba(124, 58, 237, 0.25);
}
.hero h1 { margin: 0; font-size: 2.6rem; font-weight: 800; }
.grad {
    background: linear-gradient(90deg, #F5B841, #FF5C7A);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { margin: 6px 0 0; color: #B8BFD0; }

div[data-testid="stMetric"] {
    background: rgba(26, 31, 43, 0.55);
    backdrop-filter: blur(10px);
    border: 1px solid #2B3345;
    border-left: 4px solid #F5B841;
    padding: 16px; border-radius: 14px;
}
.alert-card {
    padding: 14px 18px; border-radius: 14px; margin-bottom: 10px;
    background: rgba(26, 31, 43, 0.55);
    backdrop-filter: blur(10px);
    border: 1px solid #2B3345; border-left: 5px solid;
}
.alert-high { border-left-color: #FF5C7A; }
.alert-mid { border-left-color: #F5B841; }
.alert-ok { border-left-color: #1ED3B0; }
</style>
""", unsafe_allow_html=True)


def card(kind, text):
    st.markdown(f'<div class="alert-card alert-{kind}">{text}</div>', unsafe_allow_html=True)


def style(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        legend_title_text="",
    )
    return fig


# ---------- Load data ----------
conn = sqlite3.connect("data/smartalert.db")
df = pd.read_sql("SELECT * FROM transactions", conn)
budgets = pd.read_sql("SELECT * FROM budgets", conn)
conn.close()
df["month"] = df["date"].str[:7]
df["dt"] = pd.to_datetime(df["date"])

# ---------- Sidebar controls ----------
st.sidebar.title("🎛️ Controls")
months = sorted(df["month"].unique(), reverse=True)
selected = st.sidebar.selectbox("Month", months)
categories = sorted(df["category"].unique())
chosen = st.sidebar.multiselect("Categories", categories, default=categories)
multiplier = st.sidebar.slider("Spike sensitivity (x average)", 1.5, 4.0, 2.0, 0.5)
st.sidebar.caption("Lower = more alerts. Higher = only huge payments.")

month_df = df[df["month"] == selected]
view = month_df[month_df["category"].isin(chosen)]
month_spend = month_df.groupby("category")["amount"].sum()

spent_now = int(view["amount"].sum())
idx = months.index(selected)
delta = None
if idx + 1 < len(months):
    prev_df = df[(df["month"] == months[idx + 1]) & (df["category"].isin(chosen))]
    delta = spent_now - int(prev_df["amount"].sum())

# ---------- Alerts ----------
df["category_avg"] = df.groupby("category")["amount"].transform("mean")
df["ratio"] = df["amount"] / df["category_avg"]

spikes = df[(df["amount"] > multiplier * df["category_avg"]) & (df["category"].isin(chosen))]

subs = df[df["category"] == "Subscription"].groupby(["merchant", "amount"]).size().reset_index(name="times_paid")
subs = subs[subs["times_paid"] >= 2]
if "Subscription" not in chosen:
    subs = subs.iloc[0:0]

model = IsolationForest(contamination=0.02, random_state=42)
model.fit(df[["amount", "ratio"]])
df["score"] = model.decision_function(df[["amount", "ratio"]])
unusual = df[(df["score"] < -0.1) & (df["category"].isin(chosen))].sort_values("score")

budgets_view = budgets[budgets["category"].isin(chosen)]
over_budget = sum(
    int(month_spend.get(r["category"], 0)) > r["budget"] for _, r in budgets_view.iterrows()
)
total_alerts = over_budget + len(spikes) + len(subs) + len(unusual)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <h1><span class="grad">SmartAlert</span> 💸</h1>
  <p>Proactive spending intelligence. It warns you before a small problem becomes a big one.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric(f"Spent in {selected}", f"{spent_now:,}", delta=delta, delta_color="inverse")
c2.metric("Transactions", len(view))
c3.metric("Budgets exceeded", f"{over_budget} / {len(budgets_view)}")
c4.metric("Active alerts 🚨", total_alerts)

st.write("")
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Budgets", "🚨 Alerts", "🔍 Explore"])

# ---------- Overview ----------
with tab1:
    if view.empty:
        st.info("No data for these filters. Pick at least one category.")
    else:
        left, right = st.columns(2)
        with left:
            st.subheader("Where your money went")
            spend = view.groupby("category")["amount"].sum().reset_index()
            fig = px.pie(spend, names="category", values="amount", hole=0.55,
                         color_discrete_sequence=PALETTE)
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(style(fig))
        with right:
            st.subheader("Daily spending")
            daily = view.groupby("dt")["amount"].sum().reset_index()
            fig = px.area(daily, x="dt", y="amount", color_discrete_sequence=[GOLD])
            fig.update_layout(xaxis_title="", yaxis_title="")
            st.plotly_chart(style(fig))

        st.subheader("Every payment (red circles = flagged by AI)")
        fig = px.scatter(view, x="dt", y="amount", color="category",
                         hover_data=["merchant", "date"], color_discrete_sequence=PALETTE)
        flagged = unusual[unusual["month"] == selected]
        if not flagged.empty:
            fig.add_trace(go.Scatter(
                x=flagged["dt"], y=flagged["amount"], mode="markers", name="AI flagged",
                marker=dict(size=18, color="rgba(0,0,0,0)", line=dict(color=RED, width=3)),
                hovertext=flagged["merchant"],
            ))
        fig.update_layout(xaxis_title="", yaxis_title="")
        st.plotly_chart(style(fig))

# ---------- Budgets ----------
with tab2:
    st.subheader(f"Budget tracker ({selected})")
    for _, row in budgets_view.iterrows():
        spent = int(month_spend.get(row["category"], 0))
        budget = int(row["budget"])
        pct = spent / budget if budget else 0
        if spent > budget:
            st.markdown(f"🔴 **{row['category']}** — {spent:,} of {budget:,} (over by {spent - budget:,})")
        elif pct > 0.8:
            st.markdown(f"🟡 **{row['category']}** — {spent:,} of {budget:,} (almost there)")
        else:
            st.markdown(f"🟢 **{row['category']}** — {spent:,} of {budget:,}")
        st.progress(min(pct, 1.0))

# ---------- Alerts ----------
with tab3:
    st.subheader("Budget alerts")
    shown = False
    for _, row in budgets_view.iterrows():
        spent = int(month_spend.get(row["category"], 0))
        if spent > row["budget"]:
            card("high", f"🔴 <b>{row['category']}</b> budget is {row['budget']:,}, you spent {spent:,}")
            shown = True
    if not shown:
        card("ok", "✅ All budgets are on track.")

    st.subheader("Spike alerts")
    if spikes.empty:
        card("ok", "✅ No unusual spikes.")
    for _, r in spikes.iterrows():
        card("mid", f"⚡ <b>{r['category']}</b> payment of {r['amount']:,} at {r['merchant']} on {r['date']} is more than {multiplier}x the usual average")

    st.subheader("Subscription alerts")
    if subs.empty:
        card("ok", "✅ No repeated subscriptions.")
    for _, r in subs.iterrows():
        card("mid", f"🔁 You paid <b>{r['merchant']}</b> {r['amount']} {r['times_paid']} times. Is this a subscription you still need?")

    st.subheader("🤖 AI anomaly detection (Isolation Forest)")
    if unusual.empty:
        card("ok", "✅ The model found nothing unusual.")
    for _, r in unusual.iterrows():
        card("high", f"🤖 <b>{r['merchant']}</b> {r['amount']:,} ({r['category']}) on {r['date']} looks unusual. Anomaly score: {r['score']:.3f}")

# ---------- Explore ----------
with tab4:
    st.subheader("Search your transactions")
    q = st.text_input("Search by merchant (e.g. Amazon)")
    table = view[["date", "merchant", "amount", "category"]].sort_values("date", ascending=False)
    if q:
        table = table[table["merchant"].str.contains(q, case=False)]
    st.dataframe(table)
    st.download_button("⬇️ Download as CSV", table.to_csv(index=False), "transactions.csv", "text/csv")