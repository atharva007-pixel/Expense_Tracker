# Expense_Tracker
# 💰 Expense Tracker (Python + Streamlit)

A simple, free, self-contained expense tracker built with Streamlit and SQLite.
No API keys, no paid services — everything runs locally or on free hosting.

## Features
- Add expenses with date, category, description, and amount
- Filter by date range, category, and search text
- Summary metrics: total spent, number of expenses, average expense
- Charts: spending by category (pie), spending over time (line), monthly totals (bar)
- Delete individual expenses
- Export filtered data to CSV
- Data persisted locally in a SQLite database (`expenses.db`)

## Run locally

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/expense-tracker.git
   cd expense-tracker
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

5. Open the URL shown in the terminal (usually `http://localhost:8501`).

## Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: expense tracker app"
git branch -M main
git remote add origin https://github.com/<your-username>/expense-tracker.git
git push -u origin main
```

Note: `expenses.db` is in `.gitignore` so your personal data won't be pushed to GitHub.

## Deploy for free (Streamlit Community Cloud)

1. Push this repo to GitHub (see above).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click "New app", select this repo and branch, set the main file to `app.py`.
4. Click "Deploy". You'll get a free public URL.

> Note: on Streamlit Community Cloud, the filesystem resets whenever the app restarts/redeploys, so the SQLite database is not permanent storage there. For a class project or portfolio demo this is fine. If you want persistent hosted storage later, you could swap in a free-tier hosted database (e.g. Supabase's free Postgres tier).

## Project structure
```
expense-tracker/
├── app.py              # main Streamlit app
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

## Tech stack
- [Streamlit](https://streamlit.io/) – UI framework
- [SQLite](https://www.sqlite.org/) – local database (built into Python, no setup needed)
- [Pandas](https://pandas.pydata.org/) – data handling
- [Plotly](https://plotly.com/python/) – interactive charts
