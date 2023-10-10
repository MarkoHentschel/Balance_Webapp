import streamlit as st
import plotly.graph_objects as go

import calendar
from datetime import datetime

# --- Initial Settings and mappings for the st webapp ---
currency = "EUR"
page_title = "Income and Expense Tracker"
#page_icon = ":money_bag:" # buggy atm, maybe add later https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

income_type = ["Salary", "Other Income"]
expenses_type = ["Rent", "Mobility", "Groceries", "Utilities", "Travel", "Fun", "Other Expenses"]

input_month = list(calendar.month_name[1:])
input_year = [datetime.today().year, datetime.today().year - 1, datetime.today().year + 1]


# --------------------------------------------------------

st.set_page_config(page_title=page_title, layout=layout)
st.title(page_title)

# --- date dropdown for balance input ---

st.header(f"Data Entry in {currency}")
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox("Select Month:", input_month, key="month")
    col2.selectbox("Select Year:", input_year, key="year")

    "---"  #this is a optical divider
    with st.expander("Income"):
        for income in income_type:
            st.number_input(f"{income}:", min_value=0.0, format="%f", step=1.0, key=income)
            
    with st.expander("Expenses"):
        for expense in expenses_type:
            st.number_input(f"{expense}:", min_value=0.0, format="%f", step=1.0, key=expense)
 
    with st.expander("Comment"):
        comment = st.text_area("", placeholder="Enter a comment for the balance entry")
 
    "---"  #this is a optical divider
    submitted = st.form_submit_button("Save Entry")
    if submitted:
        period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
        income_type = {income: st.session_state[income] for income in income_type}
        expenses_type = {expense: st.session_state[expense] for expense in expenses_type}
        
        
