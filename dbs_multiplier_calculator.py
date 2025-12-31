import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------------
# DBS Multiplier Configuration
# -----------------------------
BASE_RATE = 0.0005  # 0.05% p.a.
MIN_TXN = 500

# Bonus tiers: (min_txn, max_txn, categories, rate, cap)
# Categories EXCLUDE salary
BONUS_TIERS = [
    (500, 14999, 1, 0.018, 50000),
    (15000, 29999, 1, 0.019, 50000),
    (30000, 999999, 1, 0.022, 50000),

    (500, 14999, 2, 0.021, 100000),
    (15000, 29999, 2, 0.022, 100000),
    (30000, 999999, 2, 0.030, 100000),

    (500, 14999, 3, 0.024, 100000),
    (15000, 29999, 3, 0.025, 100000),
    (30000, 999999, 3, 0.041, 100000),
]

# -----------------------------
# Core Calculation Logic
# -----------------------------
def calculate_interest(balance, salary, other_transactions):
    """
    salary: float (included in total txn, excluded from category count)
    other_transactions: list of floats (each >0 counts as a category)
    """

    total_txn = salary + sum(other_transactions)
    categories = sum(1 for t in other_transactions if t > 0)

    bonus_rate = BASE_RATE
    bonus_cap = 0

    if total_txn >= MIN_TXN and categories > 0:
        for min_txn, max_txn, cats, rate, cap in BONUS_TIERS:
            if (
                min_txn <= total_txn <= max_txn
                and categories >= cats
            ):
                bonus_rate = rate
                bonus_cap = cap

    bonus_balance = min(balance, bonus_cap)
    excess_balance = max(balance - bonus_balance, 0)

    monthly_bonus_interest = bonus_balance * bonus_rate / 12
    monthly_base_interest = excess_balance * BASE_RATE / 12

    total_monthly_interest = monthly_bonus_interest + monthly_base_interest

    return {
        "total_txn": total_txn,
        "categories": categories,
        "bonus_rate": bonus_rate * 100,
        "bonus_cap": bonus_cap,
        "monthly_interest": total_monthly_interest
    }

# -----------------------------
# GUI Callback
# -----------------------------
def run_calculator():
    try:
        balance = float(balance_entry.get())
        salary = float(salary_entry.get())

        other_txns = [
            float(card_entry.get()),
            float(home_entry.get()),
            float(insurance_entry.get()),
            float(invest_entry.get()),
        ]

        result = calculate_interest(balance, salary, other_txns)

        output.set(
            f"Total Eligible Transactions: S${result['total_txn']:.2f}\n"
            f"Qualified Categories (excl. salary): {result['categories']}\n"
            f"Bonus Interest Rate: {result['bonus_rate']:.2f}% p.a.\n"
            f"Bonus Balance Cap: S${result['bonus_cap']}\n\n"
            f"Total Monthly Interest:\n"
            f"S${result['monthly_interest']:.2f}"
        )

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# -----------------------------
# Tkinter UI Setup
# -----------------------------
root = tk.Tk()
root.title("DBS Multiplier Account Calculator")
root.geometry("480x520")
root.resizable(False, False)

main = ttk.Frame(root, padding=15)
main.pack(fill="both", expand=True)

ttk.Label(main, text="DBS Multiplier Calculator", font=("Arial", 14, "bold")).pack(pady=10)

def labeled_entry(label):
    frame = ttk.Frame(main)
    frame.pack(fill="x", pady=3)
    ttk.Label(frame, text=label, width=30).pack(side="left")
    entry = ttk.Entry(frame)
    entry.pack(side="right", fill="x", expand=True)
    entry.insert(0, "0")
    return entry

balance_entry = labeled_entry("Average Daily Balance (S$)")
salary_entry = labeled_entry("Salary Credit (Not a Category)")
card_entry = labeled_entry("Credit Card Spend")
home_entry = labeled_entry("Home Loan")
insurance_entry = labeled_entry("Insurance")
invest_entry = labeled_entry("Investments")

ttk.Button(main, text="Calculate Interest", command=run_calculator).pack(pady=15)

output = tk.StringVar()
ttk.Label(main, textvariable=output, font=("Arial", 10), justify="left").pack(pady=10)

root.mainloop()
