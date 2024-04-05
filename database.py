import psycopg2
import bcrypt
import binascii


DATABASE_CONFIG={
    'database':'expense',
    'user':'postgres',
    'password':'root',
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

