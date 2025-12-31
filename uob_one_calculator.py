import tkinter as tk
from tkinter import ttk, messagebox

BASE_RATE = 0.0005
SPEND_ONLY_RATE = 0.0065  # 0.65% p.a.

UOB_TIERS = [
    (75000, 0.0100),   # Tiered paths only
    (50000, 0.0200),
    (25000, 0.0005),
]

def calculate_uob_one(balance, salary, spend, giro_count):
    # Individual conditions
    spend_ok = spend >= 500
    giro_ok = giro_count >= 3
    salary_ok = salary >= 1600

    # Qualifying paths
    path_spend_only = spend_ok
    path_spend_giro = spend_ok and giro_ok
    path_salary_spend = salary_ok and spend_ok

    # Tiered paths take precedence over spend-only
    use_tiered = path_spend_giro or path_salary_spend
    use_spend_only = path_spend_only and not use_tiered

    interest = 0.0
    bonus_balance_used = 0.0
    interest_model = "Base"

    if use_tiered:
        remaining = min(balance, 150000)
        bonus_balance_used = remaining
        interest_model = "Tiered (Spend+GIRO / Salary+Spend)"

        for cap, rate in UOB_TIERS:
            tier_amt = min(remaining, cap)
            interest += tier_amt * rate / 12
            remaining -= tier_amt
            if remaining <= 0:
                break

        if balance > 150000:
            interest += (balance - 150000) * BASE_RATE / 12

    elif use_spend_only:
        bonus_balance_used = balance
        interest_model = "Spend Only (0.65%)"
        interest = balance * SPEND_ONLY_RATE / 12

    else:
        interest_model = "Base (No Qualification)"
        interest = balance * BASE_RATE / 12

    effective_rate = (interest * 12 / balance * 100) if balance > 0 else 0

    return {
        "path_spend_only": path_spend_only,
        "path_spend_giro": path_spend_giro,
        "path_salary_spend": path_salary_spend,
        "interest_model": interest_model,
        "bonus_balance": bonus_balance_used,
        "interest": interest,
        "effective_rate": effective_rate
    }

def run_uob():
    try:
        balance = float(balance_entry.get())
        salary = float(salary_entry.get())
        spend = float(spend_entry.get())
        giro = int(giro_entry.get())

        r = calculate_uob_one(balance, salary, spend, giro)

        output.set(
            f"Qualifying Paths:\n"
            f"Card Spend Only: {'YES' if r['path_spend_only'] else 'NO'}\n"
            f"Spend + 3 GIRO: {'YES' if r['path_spend_giro'] else 'NO'}\n"
            f"Salary + Spend: {'YES' if r['path_salary_spend'] else 'NO'}\n\n"
            f"Interest Model Used:\n{r['interest_model']}\n\n"
            f"Bonus Balance Used: S${r['bonus_balance']:,.0f}\n"
            f"Effective Interest Rate: {r['effective_rate']:.2f}% p.a.\n"
            f"Monthly Interest: S${r['interest']:,.2f}"
        )

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# -----------------------------
# Tkinter UI
# -----------------------------
root = tk.Tk()
root.title("UOB One Account Calculator")
root.geometry("540x520")
root.resizable(False, False)

frame = ttk.Frame(root, padding=15)
frame.pack(fill="both", expand=True)

def labeled_entry(label):
    f = ttk.Frame(frame)
    f.pack(fill="x", pady=4)
    ttk.Label(f, text=label, width=32).pack(side="left")
    e = ttk.Entry(f)
    e.pack(side="right", fill="x", expand=True)
    e.insert(0, "0")
    return e

balance_entry = labeled_entry("Average Balance (S$)")
salary_entry = labeled_entry("Salary Credit (S$)")
spend_entry = labeled_entry("Card Spend (S$)")
giro_entry = labeled_entry("Number of GIRO Transactions")

ttk.Button(frame, text="Calculate", command=run_uob).pack(pady=12)

output = tk.StringVar()
ttk.Label(frame, textvariable=output, justify="left").pack(pady=8)

root.mainloop()
