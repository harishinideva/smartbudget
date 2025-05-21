import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

EXPENSE_FILE = "expenses.csv"

# Initialize expenses CSV if not exists
if not os.path.exists(EXPENSE_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])
    df.to_csv(EXPENSE_FILE, index=False)

# Functions


def add_expense(date, category, amount):
    df = pd.read_csv(EXPENSE_FILE)
    new_entry = pd.DataFrame([[date, category, amount]], columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(EXPENSE_FILE, index=False)


def view_expenses():
    return pd.read_csv(EXPENSE_FILE)


def delete_expense(index):
    df = pd.read_csv(EXPENSE_FILE)
    df = df.drop(index).reset_index(drop=True)
    df.to_csv(EXPENSE_FILE, index=False)


def plot_summary(df):
    st.subheader("📊 Category-wise Summary")
    summary = df.groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    summary.plot(kind='bar', ax=ax, color='skyblue')
    st.pyplot(fig)


def monthly_summary(df):
    st.subheader("📅 Monthly Summary")
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")
    summary = df.groupby("Month")["Amount"].sum()
    st.bar_chart(summary)


def calculate_savings(df, total_budget):
    total_spent = df["Amount"].sum()
    remaining = total_budget - total_spent
    st.metric(label="💸 Total Spent", value=f"₹{total_spent:.2f}")
    st.metric(label="💰 Remaining Balance", value=f"₹{remaining:.2f}")
    return total_spent, remaining


# Streamlit App UI
st.title("💸 SmartBudget – Personal Expense Tracker")

# Sidebar to enter budget
st.sidebar.header("Set Your Budget 💰")
total_budget = st.sidebar.number_input(
    "Enter your total amount available (₹)", min_value=0.0, value=10000.0, step=500.0)

# Menu
menu = st.sidebar.radio("Menu", [
    "➕ Add Expense",
    "📂 View Expenses",
    "📈 Category Summary",
    "📅 Monthly Summary",
    "💰 Budget Summary",
    "🗑️ Delete Expense"
])

if menu == "➕ Add Expense":
    st.header("➕ Add New Expense")
    date = st.date_input("Date", datetime.today())
    category = st.selectbox(
        "Category", ["Food", "Transport", "Rent", "Bills", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    if st.button("Add Expense"):
        add_expense(str(date), category, amount)
        st.success("✅ Expense added successfully!")

elif menu == "📂 View Expenses":
    st.header("📂 All Expenses")
    df = view_expenses()
    st.dataframe(df)

elif menu == "📈 Category Summary":
    df = view_expenses()
    if df.empty:
        st.warning("No expenses to show.")
    else:
        plot_summary(df)

elif menu == "📅 Monthly Summary":
    df = view_expenses()
    if df.empty:
        st.warning("No data available.")
    else:
        monthly_summary(df)

elif menu == "💰 Budget Summary":
    df = view_expenses()
    if df.empty:
        st.warning("Add some expenses first.")
    else:
        st.header("💰 Budget and Balance")
        st.metric(label="🧾 Total Budget", value=f"₹{total_budget:.2f}")
        calculate_savings(df, total_budget)

elif menu == "🗑️ Delete Expense":
    df = view_expenses()
    st.header("🗑️ Delete Expense")
    if df.empty:
        st.warning("No expenses to delete.")
    else:
        st.dataframe(df)
        index_to_delete = st.number_input(
            "Enter Row Number to Delete", min_value=0, max_value=len(df)-1)
        if st.button("Delete"):
            delete_expense(index_to_delete)
            st.success("Deleted successfully!")
