#!/usr/bin/env python3
"""
Simple Transportation Data Manager
Add entries and visualize cost coverage
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# HARDCODED SETTINGS
CSV_FILE = "2025_09_25.csv"
SUBSCRIPTION_COST = 355.00


def load_data():
    """Load data from CSV file"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Date", "From", "To", "Cost_CHF"])


def save_data(df):
    """Save DataFrame to CSV"""
    df.to_csv(CSV_FILE, index=False)
    print(f"✅ Saved to {CSV_FILE}\n")


def display_data(df):
    """Display current data"""
    if df.empty:
        print("📋 No data yet.\n")
        return

    print("\n🚂 Current Trips:")
    print("=" * 60)

    for idx, row in df.iterrows():
        date_str = pd.to_datetime(row["Date"]).strftime("%d.%m.%Y")
        print(f"{date_str}: {row['From']} → {row['To']} | {row['Cost_CHF']:.2f} CHF")

    total = df["Cost_CHF"].sum()
    remaining = SUBSCRIPTION_COST - total
    coverage = (total / SUBSCRIPTION_COST) * 100

    print("=" * 60)
    print(f"💰 Total: {total:.2f} CHF")
    print(f"🎯 Subscription: {SUBSCRIPTION_COST:.2f} CHF")
    print(f"📊 Coverage: {coverage:.1f}%")

    if remaining > 0:
        print(f"🔴 Need {remaining:.2f} CHF more to break even\n")
    else:
        print(f"🟢 Exceeded by {abs(remaining):.2f} CHF\n")


def add_entry(df):
    """Add a new trip"""
    print("\n➕ Add new trip:")

    # Date
    date_input = input("Date (DD.MM.YYYY or Enter for today): ").strip()
    if not date_input:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            date_obj = datetime.strptime(date_input, "%d.%m.%Y")
            date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date, using today")
            date = datetime.now().strftime("%Y-%m-%d")

    # From and To
    from_loc = input("From: ").strip()
    to_loc = input("To: ").strip()

    # Cost
    try:
        cost = float(input("Cost (CHF): ").strip())
    except ValueError:
        print("❌ Invalid cost")
        return df

    # Add to dataframe
    new_row = pd.DataFrame(
        {"Date": [date], "From": [from_loc], "To": [to_loc], "Cost_CHF": [cost]}
    )

    df = pd.concat([df, new_row], ignore_index=True)
    print(f"✅ Added: {from_loc} → {to_loc} ({cost:.2f} CHF)")

    save_data(df)
    return df


def plot_coverage(df):
    """Plot pie chart of coverage"""
    if df.empty:
        print("❌ No data to plot\n")
        return

    total = df["Cost_CHF"].sum()
    remaining = max(0, SUBSCRIPTION_COST - total)
    exceeded = max(0, total - SUBSCRIPTION_COST)

    if exceeded > 0:
        labels = ["Break-even amount", "Excess usage"]
        sizes = [SUBSCRIPTION_COST, exceeded]
        colors = ["#2E8B57", "#FF6347"]
        title = f"Total: {total:.2f} CHF (Exceeded by {exceeded:.2f} CHF)"
    else:
        labels = ["Used", "Remaining"]
        sizes = [total, remaining]
        colors = ["#4169E1", "#D3D3D3"]
        title = f"Total: {total:.2f} CHF ({remaining:.2f} CHF to break even)"

    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 12},
    )

    plt.title(
        f"Transportation vs {SUBSCRIPTION_COST:.2f} CHF Subscription\n{title}",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )

    plt.axis("equal")
    plt.tight_layout()
    plt.show()


def main():
    """Main program"""
    df = load_data()

    while True:
        print(f"\n🚂 Transport Manager - {CSV_FILE}")
        print("1. 📋 Show data")
        print("2. ➕ Add trip")
        print("3. 📊 Plot chart")
        print("4. 🚪 Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            display_data(df)
        elif choice == "2":
            df = add_entry(df)
        elif choice == "3":
            plot_coverage(df)
        elif choice == "4":
            print("👋 Bye!")
            break
        else:
            print("❌ Invalid choice\n")


if __name__ == "__main__":
    main()
