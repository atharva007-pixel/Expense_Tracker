import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import plotly.express as px

# ---------- CONFIG ----------
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")
DB_FILE = "expenses.db"
CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Entertainment",
              "Health", "Shopping", "Education", "Other"]

# ---------- DATABASE ----------
def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_expense(exp_date, category, description, amount):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
        (exp_date.isoformat(), category, description, amount)
    )
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def load_expenses():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
    conn.close()
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df

init_db()

# ---------- SIDEBAR: ADD EXPENSE ----------
st.sidebar.header("➕ Add Expense")
with st.sidebar.form("add_expense_form", clear_on_submit=True):
    exp_date = st.date_input("Date", value=date.today())
    category = st.selectbox("Category", CATEGORIES)
    description = st.text_input("Description (optional)")
    amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if amount <= 0:
            st.sidebar.error("Amount must be greater than 0.")
        else:
            add_expense(exp_date, category, description, amount)
            st.sidebar.success("Expense added!")

# ---------- MAIN ----------
st.title("💰 Expense Tracker")

df = load_expenses()

if df.empty:
    st.info("No expenses yet. Add one from the sidebar to get started.")
else:
    # --- Filters ---
    with st.expander("🔍 Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            min_date = df["date"].min().date()
            max_date = df["date"].max().date()
            date_range = st.date_input("Date range", (min_date, max_date))
        with col2:
            selected_categories = st.multiselect("Categories", CATEGORIES, default=CATEGORIES)
        with col3:
            search_text = st.text_input("Search description")

    filtered_df = df.copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start) & (filtered_df["date"].dt.date <= end)
        ]
    if selected_categories:
        filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]
    if search_text:
        filtered_df = filtered_df[
            filtered_df["description"].str.contains(search_text, case=False, na=False)
        ]

    # --- Summary metrics ---
    total_spent = filtered_df["amount"].sum()
    avg_expense = filtered_df["amount"].mean() if not filtered_df.empty else 0
    num_expenses = len(filtered_df)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Spent", f"${total_spent:,.2f}")
    m2.metric("Number of Expenses", num_expenses)
    m3.metric("Average Expense", f"${avg_expense:,.2f}")

    st.divider()

    # --- Charts ---
    if not filtered_df.empty:
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Spending by Category")
            cat_summary = filtered_df.groupby("category")["amount"].sum().reset_index()
            fig_pie = px.pie(cat_summary, names="category", values="amount", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.subheader("Spending Over Time")
            time_summary = filtered_df.groupby(filtered_df["date"].dt.date)["amount"].sum().reset_index()
            time_summary.columns = ["date", "amount"]
            fig_line = px.line(time_summary, x="date", y="amount", markers=True)
            st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("Monthly Totals")
        monthly = filtered_df.copy()
        monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
        monthly_summary = monthly.groupby("month")["amount"].sum().reset_index()
        fig_bar = px.bar(monthly_summary, x="month", y="amount")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- Table + delete ---
    st.subheader("📋 All Expenses")
    display_df = filtered_df.copy()
    display_df["date"] = display_df["date"].dt.date

    for _, row in display_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 2.5, 1, 0.6])
        col1.write(str(row["date"]))
        col2.write(row["category"])
        col3.write(row["description"] if row["description"] else "—")
        col4.write(f"${row['amount']:.2f}")
        if col5.button("🗑️", key=f"del_{row['id']}"):
            delete_expense(row["id"])
            st.rerun()

    # --- Export ---
    st.download_button(
        "⬇️ Download CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="expenses.csv",
        mime="text/csv",
    )