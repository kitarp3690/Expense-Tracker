import streamlit as st
import pandas as pd
import database as db
import plotly.express as px
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def display_income_trend():
    st.subheader('Income Trend')
    # Fetch income data over time from the database
    income_data = db.get_income_trend()
    if income_data:
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(income_data, columns=['Date', 'Amount'])
        # Display line chart for income trend
        fig = px.line(df, x='Date', y='Amount', title='Income Trend')
        fig.update_traces(mode='lines+markers')
        st.plotly_chart(fig)

def display_expense_trend():
    st.subheader('Expense Trend')
    # Fetch expense data over time from the database
    expense_data = db.get_expense_trend()
    if expense_data:
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(expense_data, columns=['Date', 'Amount'])
        # Display line chart for expense trend
        fig = px.line(df, x='Date', y='Amount', title='Expense Trend')
        fig.update_traces(mode='lines+markers')
        st.plotly_chart(fig)

def display_expense_distribution():
    st.subheader('Expense Distribution')
    # Fetch expense distribution data from the database
    expense_distribution = db.get_expense_distribution()
    if expense_distribution:
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(expense_distribution, columns=['Category', 'Amount'])
        # Display pie chart for expense distribution
        fig = px.pie(df, values='Amount', names='Category', title='Expense Distribution')
        st.plotly_chart(fig)

def generate_pdf_chart(chart):
    # Convert Plotly chart to PNG image
    chart_image = BytesIO()
    chart.write_image(chart_image, format='png')
    return chart_image

def export_to_pdf(dataframe, chart):
    # Generate PDF report
    st.write("Exporting to PDF...")
    pdf = BytesIO()
    plt.figure(figsize=(8, 6))
    plt.title('Report')
    plt.axis('off')

    # Write dataframe to PDF
    st.write(dataframe)
    dataframe_table = dataframe.to_string()
    plt.table(cellText=[[dataframe_table]], loc='center')

    # Write chart to PDF
    chart_image = generate_pdf_chart(chart)
    plt.imshow(plt.imread(chart_image), aspect='auto')
    plt.axis('off')

    plt.savefig(pdf, format='pdf', bbox_inches='tight')
    plt.close()

    # Download PDF
    pdf.seek(0)
    st.download_button(label='Download PDF', data=pdf, file_name='report.pdf', mime='application/pdf')

def display_report():
    st.title("Reports")
    col1, col2 = st.columns([1, 4])

    with col1:
        st.sidebar.header('Options')
        selected_option = st.sidebar.radio('Select an option', ['Income Trend', 'Expense Trend', 'Expense Distribution'])

        # Dynamic Date Range Selection
        date_range_options = st.sidebar.selectbox("Select Date Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days"])
        end_date = datetime.today()
        if date_range_options == "Last 7 Days":
            start_date = end_date - timedelta(days=7)
        elif date_range_options == "Last 30 Days":
            start_date = end_date - timedelta(days=30)
        elif date_range_options == "Last 90 Days":
            start_date = end_date - timedelta(days=90)

    with col2:
        if selected_option == 'Income Trend':
            income_data = db.get_income_trend(start_date, end_date)
            if income_data:
                df = pd.DataFrame(income_data, columns=['Date', 'Amount'])
                fig = px.line(df, x='Date', y='Amount', title='Income Trend')
                fig.update_traces(mode='lines+markers')
                st.plotly_chart(fig)
                if st.button("Export to PDF"):
                    export_to_pdf(df, fig)
            else:
                st.warning("No income data available for the selected period.")
        elif selected_option == 'Expense Trend':
            expense_data = db.get_expense_trend(start_date, end_date)
            if expense_data:
                df = pd.DataFrame(expense_data, columns=['Date', 'Amount'])
                fig = px.line(df, x='Date', y='Amount', title='Expense Trend')
                fig.update_traces(mode='lines+markers')
                st.plotly_chart(fig)
                if st.button("Export to PDF"):
                    export_to_pdf(df, fig)
            else:
                st.warning("No expense data available for the selected period.")
        elif selected_option == 'Expense Distribution':
            expense_distribution = db.get_expense_distribution()
            if expense_distribution:
                df = pd.DataFrame(expense_distribution, columns=['Category', 'Amount'])
                fig = px.pie(df, values='Amount', names='Category', title='Expense Distribution')
                st.plotly_chart(fig)
                if st.button("Export to PDF"):
                    export_to_pdf(df, fig)
            else:
                st.warning("No expense distribution data available.")


#-----------------------------------PratikTheGod---------------
def show_bar_graph_income(username:str, date:datetime):
    """This function shows the bar graph of income category\n
    Args:
        username: User's username
        date: Of which date to show bargraph\n
    Return:
        Prints the graph of income category
    """
    con=db.db_connect()
    cursor=con.cursor()
    cursor.execute("select category,amount from income where username=%s and date=%s",(username,date))
    rows=cursor.fetchall()
    rows=dict(rows)
    st.write(rows)
    x_axis=[]
    y_axis=[]
    for key,value in rows.items():
        x_axis.append(key)
        y_axis.append(value)
    data={
        "Category":x_axis,
        "Amount":y_axis
    }
    st.write(data)
    data=pd.DataFrame(data)
    st.write(data)
    data=data.set_index("Category")
    st.write(data)
    st.bar_chart(data)

def show_menu():
    st.subheader("Single day income")
    
if __name__ == '__main__':
    show_bar_graph_income('admin','2024-04-12')
    # pass
