import psycopg2
import bcrypt
import binascii
from datetime import datetime, timedelta
import streamlit as st

DATABASE_CONFIG={
    'database':'expense',
    'user':'postgres',
    'password':'admin',
    'host':'localhost',
    'port':'5432'
}

def db_connect():
    conn=psycopg2.connect(**DATABASE_CONFIG)
    return conn 

def get_one(query,place):
    '''
    Function to fetch single tuple from database. 

    Parameters:
        query: Any valid sql query 
        place: plaeholder (st.empty) to display the message 

    Returns:
        Output tuple. 
    '''
    conn=db_connect() 
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            result=cur.fetchone()
    except (Exception,psycopg2.DatabaseError) as error:
         place.error(error)
    finally:
        if conn is not None:
            cur.close() 
            conn.close() 
        return result

def get_all(query,place):
    '''
    Function to fetch all tuple from database. 

    Parameters:
    query: Any valid sql query 
    place: plaeholder (st.empty) to display the message 

    Returns:
    Output tuple. 
    '''
    conn=db_connect() 
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            result=cur.fetchall()
    except (Exception,psycopg2.DatabaseError) as error:
         place.error(error)
    finally:
        if conn is not None:
            cur.close() 
            conn.close() 
        return result

def insert_db(query,place,msg=None):
    '''
    Function to add tuple to database. 

    Parameters:
    query: Any valid sql query 
    place: plaeholder (st.empty) to display the message 
    msg: Msg to display
    
    Returns:
    None  
    '''
    conn=db_connect() 
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit() 
            if msg is not None:
                place.success(msg)
    except (Exception,psycopg2.DatabaseError) as error:
         place.error(error)
    finally:
        if conn is not None:
            cur.close() 
            conn.close()  

def hash_generator(password):
    password_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    password_hashed=binascii.hexlify(password_hash).decode('utf-8')
    return password_hashed

def check_pw(password,db_pwd):
    return bcrypt.checkpw(password.encode(),binascii.unhexlify(db_pwd))

# Function to update user's password
def update_password(username, new_password):
    conn = db_connect()
    try:
        with conn.cursor() as cur:
            # Generate bcrypt hash for the new password
            password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            password_hashed = binascii.hexlify(password_hash).decode('utf-8')

            # Update the password in the database
            cur.execute("UPDATE users SET password_hash = %s WHERE username = %s", (password_hashed, username))
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error updating password:", error)
    finally:
        if conn is not None:
            conn.close()

# Function to update user's profile picture
def update_profile_picture(username, new_image,slot,msg=None):
    conn = db_connect()
    try:
        with conn.cursor() as cur:
            # Update the profile picture in the database
            cur.execute("UPDATE users SET image = %s WHERE username = %s", (psycopg2.Binary(new_image), username))
            conn.commit()
            if msg:
                slot.success(msg)
    except (Exception, psycopg2.DatabaseError) as error:
        slot.error(f"Error updating profile picture:{error}")
    finally:
        if conn is not None:
            conn.close()

def check_user_existence(username:str): 
    """This function check if username already exists or not\n
    Args:
        username: User's username
    Return:
        It returns true if username already exists in database otherwise false
    """
    try:
        con=db_connect()
        cursor=con.cursor()
        cursor.execute("select * from users where username=%s",(username,))
        result=cursor.fetchone()
        if result:
            return True
        else:
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(error)
    finally:
        if con is not None:
            con.close()