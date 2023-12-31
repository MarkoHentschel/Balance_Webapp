import os
from deta import Deta
from dotenv import load_dotenv

#--loading deta connection (database)
load_dotenv(".env")
DETA_PROJECT_KEY = os.getenv("DETA_KEY")


deta = Deta(DETA_PROJECT_KEY)

db = deta.Base("monthly_reports")

def insert_period(period, incomes, expenses, comment):
    return db.put({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})

def fetch_all_periods():
    res = db.fetch()
    return res.items

def get_period(period):
    return db.get(period)