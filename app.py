import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import calendar
from datetime import datetime

# --- Initial Settings and mappings for the st webapp ---
currency = "EUR"
page_title = "Income and Expense Tracker"
#page_icon = ":money_bag:" # buggy atm, maybe add later https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

incomes = ["Salary", "Other Income"]
expenses = ["Rent", "Mobility", "Groceries", "Utilities", "Travel", "Fun", "Other Expenses"]

input_month = list(calendar.month_name[1:])
input_year = [datetime.today().year, datetime.today().year - 1, datetime.today().year + 1]

hide_st_style = """
            <style>
            #MainMenu {visibilitiy: hidden;}
            footer {visibilitiy: hidden;}
            header {visibilitiy: hidden;}
            </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# --------------------------------------------------------


st.title(page_title)

selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"], #for a list of icons https://icons.getbootstrap.com/
    orientation="horizontal"
)

# --- date dropdown for balance input ---
if selected == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month:", input_month, key="month")
        col2.selectbox("Select Year:", input_year, key="year")

        "---"  #this is an optical divider
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0.0, format="%f", step=1.0, key=income)
                
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0.0, format="%f", step=1.0, key=expense)
    
        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Enter a comment for the balance entry")
    
        "---"  #this is an optical divider
        submitted = st.form_submit_button("Save Entry")
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            
            st.write(f"incomes: {incomes}")
            st.write(f"expenses: {expenses}")
            st.success("Entry saved")
        
# ---- Plotting -----
if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_periods"):
        period = st.selectbox("Select Period:", ["2023_October"])
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            comment = "Some example"
            incomes = {'Salary': 1000}
            expenses = {'Rent:': 300}      
            
            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income - total_expense
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expense", f"{total_expense} {currency}")
            col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
            st.text(f"Comment: {comment}")
            
            # Create sankey chart
            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())
            
            link = dict(source = source, target = target, value = value)
            node = dict(label = label, pad=50, thickness=5, color="#E694FF")
            data = go.Sankey(link = link, node = node)

            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)
