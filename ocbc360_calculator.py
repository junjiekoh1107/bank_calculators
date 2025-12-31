import tkinter as tk
from tkinter import ttk, messagebox

BASE_RATE = 0.0005  # 0.05%

CATEGORY_RULES = {
    "salary":  {"min": 1800, "rates": (0.012, 0.024)},
    "save":    {"min": 500,  "rates": (0.004, 0.008)},
    "spend":   {"min": 500,  "rates": (0.004, 0.004)},
    "insure":  {"min": 2000, "rates": (0.012, 0.024)},
    "invest":  {"min": 2000, "rates": (0.012, 0.024)},
}

def calculate_ocbc(balance, inputs):
    bonus_rate_75 = 0.0
    bonus_rate_25 = 0.0
    qualified_categories = []

    salary_ok = inputs["salary"] >= CATEGORY_RULES["salary"]["min"]

    for k, v in CATEGORY_RULES.items():
        qualifies = inputs[k] >= v["min"]

        # Insurance & Investment require salary credit
        if k in ["insure", "invest"]:
            qualifies = qualifies and salary_ok

        if qualifies:
            bonus_rate_75 += v["rates"][0]
            bonus_rate_25 += v["rates"][1]
            qualified_categories.append(k.capitalize())

    # Bonus balance cap = S$100,000
    bal_75 = min(balance, 75000)
    bal_25 = min(max(balance - 75000, 0), 25000)
    bonus_balance_used = bal_75 + bal_25

    bonus_interest = (
        bal_75 * bonus_rate_75 / 12 +
        bal_25 * bonus_rate_25 / 12
    )

    base_interest = balance * BASE_RATE / 12
    total_interest = bonus_interest + base_interest

    effective_rate = (total_interest * 12 / balance * 100) if balance > 0 else 0

    return {
        "qualified_categories": qualified_categories,
        "interest": total_interest,
        "effective_rate": effective_rate,
        "bonus_balance": bonus_balance_used
    }

def run_ocbc():
    try:
        balance = float(balance_entry.get())
        data = {
            "salary": float(salary_entry.get()),
            "save": float(save_entry.get()),
            "spend": float(spend_entry.get()),
            "insure": float(insure_entry.get()),
            "invest": float(invest_entry.get()),
        }

        r = calculate_ocbc(balance, data)

        output.set(
            f"Qualified Categories:\n"
            f"{', '.join(r['qualified_categories']) if r['qualified_categories'] else 'None'}\n\n"
            f"Bonus Balance Used: S${r['bonus_balance']:,.0f}\n"
            f"Effective Interest Rate: {r['effective_rate']:.2f}% p.a.\n"
            f"Monthly Interest: S${r['interest']:,.2f}"
        )

    except ValueError:
        messagebox.showerror("Input Error", "Invalid input")

# ---------------- UI ----------------
root = tk.Tk()
root.title("OCBC 360 Account Calculator")
root.geometry("500x520")

frame = ttk.Frame(root, padding=15)
frame.pack(fill="both", expand=True)

def entry(label):
    f = ttk.Frame(frame)
    f.pack(fill="x", pady=4)
    ttk.Label(f, text=label, width=32).pack(side="left")
    e = ttk.Entry(f)
    e.pack(side="right", fill="x", expand=True)
    e.insert(0, "0")
    return e

balance_entry = entry("Average Balance (S$)")
salary_entry = entry("Salary Credit (S$)")
save_entry = entry("Monthly Balance Increase (S$)")
spend_entry = entry("Card Spend (S$)")
insure_entry = entry("Insurance Premium (S$)")
invest_entry = entry("Investment Amount (S$)")

ttk.Button(frame, text="Calculate", command=run_ocbc).pack(pady=12)

output = tk.StringVar()
ttk.Label(frame, textvariable=output, justify="left").pack()

root.mainloop()
