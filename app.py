import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Life Manager", layout="wide")

st.title("📊 Daily Life Manager")

# Initialize session data
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Tasks", "Expenses"])

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.subheader("📅 Today Summary")

    total_tasks = len(st.session_state.tasks)
    total_expense = sum([e['amount'] for e in st.session_state.expenses])

    col1, col2 = st.columns(2)

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Total Expense (₹)", total_expense)

# ---------------- TASKS ----------------
elif menu == "Tasks":
    st.subheader("📝 Add Task")

    task = st.text_input("Task Name")
    date = st.date_input("Due Date")

    if st.button("Add Task"):
        if task:
            st.session_state.tasks.append({
                "task": task,
                "date": str(date)
            })
            st.success("Task Added")
        else:
            st.warning("Please enter task")

    st.subheader("📋 Task List")
    if st.session_state.tasks:
        df_tasks = pd.DataFrame(st.session_state.tasks)
        st.dataframe(df_tasks)
    else:
        st.info("No tasks added")

# ---------------- EXPENSES ----------------
elif menu == "Expenses":
    st.subheader("💰 Add Expense")

    amount = st.number_input("Amount", min_value=0)
    category = st.selectbox("Category", ["Food", "Travel", "Smoking", "Other"])
    note = st.text_input("Note")

    if st.button("Add Expense"):
        if amount > 0:
            st.session_state.expenses.append({
                "amount": amount,
                "category": category,
                "note": note,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("Expense Added")
        else:
            st.warning("Enter valid amount")

    st.subheader("📊 Expense List")
    if st.session_state.expenses:
        df_exp = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df_exp)

        st.subheader("Category Summary")
        summary = df_exp.groupby("category")["amount"].sum()
        st.bar_chart(summary)
    else:
        st.info("No expenses added")
