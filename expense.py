import streamlit as st
import database as db
from datetime import datetime
import streamlit as st
from datetime import datetime

selected_list=[] 

def add_expense(user):
    if 'expense_data' not in st.session_state:
        st.session_state.expense_data = {}

    if 'expense_date' not in st.session_state:
        st.session_state.expense_date = None 
    st.write('<p style="color: green; border-bottom: 1px solid white; margin-top: -50px; font-size: 30px; font-weight: bold">Add Expense</p>', unsafe_allow_html=True)

    c2, c1 = st.columns([2, 1])
    with c2.container(border=True):
        selected_date = st.date_input("Date", max_value=datetime.today())
        st.session_state.expense_date = selected_date

        # category_options = ["Groceries", "Utilities", "Transportation", "Others"]
        placeholder=st.empty() 
        category_options=db.get_all("Select head from expense_head",placeholder)
        category=[opt[0] for opt in category_options]
        category.append('Other')
        selected_category=' '
        selected_category = st.selectbox("Category", options=category, index=None)
        if selected_category == "Other":
            selected_category = st.text_input("Enter Custom Category")
            if selected_category is not None:
                selected_category=selected_category.strip()
        amount = st.number_input("Amount", min_value=0.0, step=100.0, format="%.2f")
        if f"deduct{selected_category}" not in st.session_state:
            setattr(st.session_state, f"deduct{selected_category}", None)
        if getattr(st.session_state, f"deduct{selected_category}", True):
            d_amount = st.number_input("Deduct Expense", max_value=st.session_state.expense_data[selected_category], min_value=0.0, step=100.0, format="%.2f")
            amount -= d_amount            
        if st.button("Add Expense"):
            if selected_category not in st.session_state.expense_data and selected_category !='':
                st.session_state.expense_data[selected_category] = 0.0
            if selected_category not in category and selected_category is not None and selected_category!='':
                db.insert_db(f"Insert into expense_head(head) values('{selected_category}')",place=placeholder)
            if selected_category and amount:
                setattr(st.session_state, f"deduct{selected_category}", True)
                # Update session state with the new expense data
                st.session_state.expense_data[selected_category] += amount
                
                # Uncomment the following line to insert into database
                # db.insert_expense_record(amount, selected_date, selected_category, description)
            else:
                st.error("Please fill in both category and amount.")

    with c1:
        with st.container(border=True):
            st.write(f'<p style="color: blue; border-bottom: 1px solid white; font-size: 20px; font-weight: bold">Your Expenses: {st.session_state.expense_date}</p>', unsafe_allow_html=True)
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
            if st.button("Save Expenses", key='save to db',use_container_width=True):
                placeholder=st.empty() 
                for head,amount in st.session_state.expense_data.items():    
                    db.insert_db(f"""
                        Insert into expenses (date, category, amount, username) values ('{st.session_state.expense_date}','{head}','{amount}','{user}')
                    """,place=placeholder,msg="Expense Saved")


if __name__ == "__main__":
    # add_expense(user)
    pass 

