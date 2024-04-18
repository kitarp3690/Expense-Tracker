import streamlit as st
import pandas as pd
import database as db
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

def show_bar_graph_income_oneday(username:str, date:datetime):
    """This function shows the bar graph of one day income category\n
    Args:
        username: User's username
        date: Of which date to show bargraph\n
    Return:
        Prints the graph of income category
    """
    st.subheader(f"Income of date:{date}")
    con=db.db_connect()
    cursor=con.cursor()
    cursor.execute("select category,amount from income where username=%s and date=%s",(username,date))
    rows=cursor.fetchall()
    rows=dict(rows)
    x_axis=[]
    y_axis=[]
    for key,value in rows.items():
        x_axis.append(key)
        y_axis.append(value)
    data={
        "Category":x_axis,
        "Amount":y_axis
    }
    data=pd.DataFrame(data)
    data=data.set_index("Category")
    st.bar_chart(data)
    con.close()

def show_bar_graph_income_weekly(username:str, start_date:datetime):
    """This function shows the bar graph of weekly income category\n
    Args:
        username: User's username
        date: Of which date to show bargraph\n
    Return:
        Prints the graph of income category
    """
    end_date = start_date + timedelta(days=6)  # End date is 6 days after the start date
    
    if start_date == datetime.now().date():
        end_date = start_date # If start date is today, set end date as yesterday
    if end_date>datetime.now().date():
        end_date = datetime.now().date()

    st.subheader(f"Income for the period from {start_date} to {end_date}")
    con = db.db_connect()
    cursor = con.cursor()
    # Fetch data for the 7-day period
    cursor.execute("SELECT category, SUM(amount) FROM income WHERE username=%s AND date BETWEEN %s AND %s GROUP BY category",
                   (username, start_date, end_date))
    rows = cursor.fetchall()
    rows = dict(rows)
    x_axis = []
    y_axis = []
    for key, value in rows.items():
        x_axis.append(key)
        y_axis.append(value)
    data = {
        "Category": x_axis,
        "Amount": y_axis
    }
    data = pd.DataFrame(data)
    data = data.set_index("Category")
    st.bar_chart(data)
    con.close()

def show_bar_graph_income_monthly(username:str, start_date:datetime):
    """This function shows the bar graph of weekly Expense category\n
    Args:
        username: User's username
        date: Of which date to show bargraph\n
    Return:
        Prints the graph of Expense category
    """
    end_date = start_date + timedelta(days=30)  # End date is 6 days after the start date
    
    if start_date == datetime.now().date():
        end_date = start_date # If start date is today, set end date as yesterday
    if end_date>datetime.now().date():
        end_date=datetime.now().date()
    
    st.subheader(f"Expenses for the period from {start_date} to {end_date}")
    con = db.db_connect()
    cursor = con.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE username=%s AND date BETWEEN %s AND %s GROUP BY category",
                   (username, start_date, end_date))
    rows = cursor.fetchall()
    rows = dict(rows)
    x_axis = []
    y_axis = []
    for key, value in rows.items():
        x_axis.append(key)
        y_axis.append(value)
    data = {
        "Category": x_axis,
        "Amount": y_axis
    }
    data = pd.DataFrame(data)
    data = data.set_index("Category")
    st.bar_chart(data)
    con.close()

def show_bar_graph_expense_oneday(username:str, date:datetime):
    """This function shows the bar graph of weekly Expense category\n
    Args:
        username: User's username
        date: Of which date to show bargraph\n
    Return:
        Prints the graph of Expense category
    """
    st.subheader(f"Expense of date:{date}")
    con=db.db_connect()
    cursor=con.cursor()
    cursor.execute("select category,amount from expenses where username=%s and date=%s",(username,date))
    rows=cursor.fetchall()
    rows=dict(rows)
    x_axis=[]
    y_axis=[]
    for key,value in rows.items():
        x_axis.append(key)
        y_axis.append(value)
    data={
        "Category":x_axis,
        "Amount":y_axis
    }
    data=pd.DataFrame(data)
    data=data.set_index("Category")
    st.bar_chart(data)
    con.close()

def show_bar_graph_expense_weekly(username:str, start_date:datetime):
    """This function shows the bar graph of weekly Expense category\n
    Args:
        username: User's username
        date: Of which date to show bargraph\n
    Return:
        Prints the graph of Expense category
    """
    end_date = start_date + timedelta(days=6)  # End date is 6 days after the start date
    
    if start_date == datetime.now().date():
        end_date = start_date # If start date is today, set end date as yesterday
    
    st.subheader(f"Expenses for the period from {start_date} to {end_date}")
    con = db.db_connect()
    cursor = con.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE username=%s AND date BETWEEN %s AND %s GROUP BY category",
                   (username, start_date, end_date))
    rows = cursor.fetchall()
    rows = dict(rows)
    x_axis = []
    y_axis = []
    for key, value in rows.items():
        x_axis.append(key)
        y_axis.append(value)
    data = {
        "Category": x_axis,
        "Amount": y_axis
    }
    data = pd.DataFrame(data)
    data = data.set_index("Category")
    st.bar_chart(data)
    con.close()

def show_bar_graph_expense_monthly(username:str, start_date:datetime):
    """This function shows the bar graph of weekly Expense category\n
    Args:
        username: User's username
        date: Of which date to show bargraph\n
    Return:
        Prints the graph of Expense category
    """
    end_date = start_date + timedelta(days=30)  # End date is 6 days after the start date
    
    if start_date == datetime.now().date():
        end_date = start_date # If start date is today, set end date as yesterday
    if end_date>datetime.now().date():
        end_date=datetime.now().date()
    
    st.subheader(f"Expenses for the period from {start_date} to {end_date}")
    con = db.db_connect()
    cursor = con.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE username=%s AND date BETWEEN %s AND %s GROUP BY category",
                   (username, start_date, end_date))
    rows = cursor.fetchall()
    rows = dict(rows)
    x_axis = []
    y_axis = []
    for key, value in rows.items():
        x_axis.append(key)
        y_axis.append(value)
    data = {
        "Category": x_axis,
        "Amount": y_axis
    }
    data = pd.DataFrame(data)
    data = data.set_index("Category")
    st.bar_chart(data)
    con.close()

def show_menu():
    st.subheader("Reports")
    tab1,tab2=st.tabs(["Income","Expense"])
    with tab1:
        options =  st.radio('select',["Single Day Income","Weekly Income","Monthly Income"]) 
        if options =="Single Day Income":
            date = st.date_input(label="Date",key="Date1", max_value=datetime.today())
            show_bar_graph_income_oneday(st.session_state.loggedin_user,date)
        elif options=="Weekly Income":
            date = st.date_input(label="Starting Date",key="Date2", max_value=datetime.today())
            show_bar_graph_income_weekly(st.session_state.loggedin_user,date)
        elif options=="Monthly Income":
            date = st.date_input(label="Starting Date",key="Date6", max_value=datetime.today())
            show_bar_graph_income_monthly(st.session_state.loggedin_user,date)

    with tab2:
        options =  st.radio('select',["Single Day Expense","Weekly Expense","Monthly Expense"]) 
        if options =="Single Day Expense":
            date = st.date_input(label="Date",key="Date3", max_value=datetime.today())
            show_bar_graph_expense_oneday(st.session_state.loggedin_user,date)
        elif options=="Weekly Expense":
            date = st.date_input(label="Starting Date",key="Date4", max_value=datetime.today())
            show_bar_graph_expense_weekly(st.session_state.loggedin_user,date)
        elif options=="Monthly Expense":
            date = st.date_input(label="Starting Date",key="Date5", max_value=datetime.today())
            show_bar_graph_expense_monthly(st.session_state.loggedin_user,date)

if __name__ == '__main__':
    show_bar_graph_income_oneday('admin','2024-04-12')
    # pass
