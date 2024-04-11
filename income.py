import streamlit as st
import database as db
from datetime import datetime

def add_income_record():
    if 'expense_data' not in st.session_state:
        st.session_state.income_data = {}

    if 'expense_date' not in st.session_state:
        st.session_state.income_date = None 
    st.write('<p style="color: green; border-bottom: 1px solid white; margin-top: -50px; font-size: 30px;text-align: center;font-weight: bold">Add income</p>', unsafe_allow_html=True)
    
    c1,c2=st.columns([2,1])
    with c1.container(border=True):
        # Input fields for income information
        placeholder=st.empty() 
        amount = st.number_input("Amount", min_value=0.0, step=100.0, format="%.2f")
        selected_date = st.date_input("Date", max_value=datetime.today())
        st.session_state.income_date = selected_date
        category_options = ["Salary", "Stock", "Business"]
        selected_category = st.selectbox("Category", options=category_options + ["Other"])
        if selected_category == "Other":
            selected_category = st.text_input("Other Category")
            if selected_category is not None:
                selected_category=selected_category.strip()
        if f"increase{selected_category}" not in st.session_state:
            setattr(st.session_state, f"increase{selected_category}", None)
        description = st.text_area("Description")
        if st.button("Add income"):
            if selected_category not in st.session_state.income_data and selected_category !='':
                st.session_state.income_data[selected_category] = 0.0
            if selected_category not in category and selected_category is not None and selected_category!='':
                db.insert_db(f"Insert into income_head(head) values('{selected_category}')",place=placeholder)
            if selected_category and amount:
                setattr(st.session_state, f"increase{selected_category}", True)
                # Update session state with the new expense data
                st.session_state.income_data[selected_category] += amount
            else:
                st.error("Please fill in both category and amount.")

    with c2.container(border=True):
        st.write(f'<p style="color: blue; border-bottom: 1px solid white; font-size: 20px; font-weight: bold">Your Income: {st.session_state.income_date}</p>', unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        s1.write(f'<p style="color: black; font-size: 18px; margin-bottom: -5px; text-align: left ">Category</p>', unsafe_allow_html=True)
        s2.write(f'<p style="color: black; font-size: 18px; margin-bottom: -5px; text-align: right ">Amount</p>', unsafe_allow_html=True)
        st.write('<hr style=" margin-top: 0px; margin-bottom: 0px">', unsafe_allow_html=True)
        cs1, cs2 = st.columns(2)
        total_expense=0
        for category, expense in st.session_state.expense_data.items():
            cs1.write(f'<p style="color: black; font-size: 15px; margin-bottom: 5px;text-align: left; margin-top: -5px">{category}</p>', unsafe_allow_html=True)
            cs2.write(f'<p style="color: black; font-size: 15px; margin-bottom: 5px;text-align: right;margin-top: -5px ">{expense}</p>', unsafe_allow_html=True)
            total_expense+=float(expense)
        
        cs1.write(f'<p style="color: black; font-size: 15px; margin-bottom: 5px;text-align: left; margin-top: -5px">Total Expense: </p>', unsafe_allow_html=True)
        cs2.write(f'<p style="color: black; font-size: 15px; margin-bottom: 5px;text-align: right;margin-top: -5px ">{total_expense}</p>', unsafe_allow_html=True)
        st.write('')
        if st.button("Save Income", key='save to db',use_container_width=True):
            # placeholder=st.empty() 
            # for head,amount in st.session_state.expense_data.items():    
            #     db.insert_db(f"""
            #         Insert into expenses (date, category, amount, username) values ('{st.session_state.expense_date}','{head}','{amount}','{user}')
            #     """,place=placeholder,msg="Expense Saved")
            # if st.button("Add Record"):
                # Insert the income record into the database
            db.insert_income_record(amount, selected_date, category, description)
            st.success("Income recorded successfully.")

if __name__ == "__main__":
    # add_income_record()
    pass