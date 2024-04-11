import streamlit as st
import database as db
from datetime import datetime

def add_income_record():
    st.write('<p style="color: green; border-bottom: 1px solid white; margin-top: -50px; font-size: 30px;text-align: center;font-weight: bold">Add income</p>', unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,2.5,1])
    with c2.container(border=True):
        # Input fields for income information
        amount = st.number_input("Amount", min_value=0.0, step=100.0, format="%.2f")
        selected_date = st.date_input("Date", max_value=datetime.today())
        category_options = ["Salary", "Stock", "Business"]
        category = st.selectbox("Category", options=category_options + ["Other"])
        if category == "Other":
            category = st.text_input("Other Category")
        description = st.text_area("Description")

        # Button to add the income record
        if st.button("Add Record"):
            # Insert the income record into the database
            db.insert_income_record(amount, selected_date, category, description)
            st.success("Income recorded successfully.")

if __name__ == "__main__":
    # add_income_record()
    pass