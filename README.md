# SmartAlert 🔔

SmartAlert is a small Python project that reads your spending and warns you **before** a problem happens.

## The Problem
Banking apps show what you already spent. They don't tell you early when you are overspending, when a payment looks unusual, or when you are paying for a subscription again and again.

## What SmartAlert Does
| Feature | What it tells you |
|---|---|
| Spending summary | Total spend, spend per category, biggest transaction, average per category |
| Budget alert | A category has gone over its budget |
| Spike alert | A payment is more than 2x the usual amount for its category |
| Subscription alert | The same merchant and amount keep repeating |

## How It Works
```
transactions.csv  →  pandas analysis  →  alert rules  →  alerts in the terminal
budgets.csv
```
1. The program reads `data/transactions.csv` and `data/budgets.csv`
2. It calculates totals and averages per category
3. It checks each alert rule
4. It prints the alerts

## Project Structure
```
smartalert/
├── data/
│   ├── transactions.csv   # sample transactions (fake data)
│   └── budgets.csv        # budget for each category
├── src/
│   └── read_data.py       # main program
└── README.md
```

## How to Run
1. Clone this repository
2. Create and activate a virtual environment
```
   python -m venv venv
   venv\Scripts\activate
```
3. Install the libraries
```
   pip install pandas numpy
```
4. Run the program
```
   python src\read_data.py
```

## Sample Output
```
Budget alerts:
ALERT: Food budget is 1500, you spent 6960
OK: Travel spent 400 of 500

Spike alerts:
ALERT: Food payment of 5000 is more than 2x the usual Food average

Subscription alerts:
ALERT: You paid Netflix 299 2 times. Is this a subscription you still need?
```

## Limitations
- Uses small fake data, not real bank data
- Rules are fixed, so a one-time big purchase can cause a false alarm
- Alerts only appear in the terminal

## Roadmap
- [ ] Store data in a SQLite database with more transactions
- [ ] Add ML anomaly detection (Isolation Forest)
- [ ] Build a Streamlit dashboard with charts
- [ ] Explain alerts in plain language using GenAI

## Built With
Python, pandas, numpy

## Author
Kavya Sri