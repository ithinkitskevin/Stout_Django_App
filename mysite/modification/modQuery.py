import mysql.connector
import os
import json

global_host = global_user = global_password = global_db = None

def initialize():
    global global_host
    global global_user
    global global_password
    global global_db

    path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')

    f = open(path_to_json, "r")
    contents = f.read()
    confdata = json.loads(contents)
    conn_info = confdata.get("conn_info")  
    
    global_host = conn_info.get("host")
    global_user = conn_info.get("user")
    global_password = conn_info.get("password")
    global_db = conn_info.get("db")

def getResultFromQuery(query):
    if global_host is None or global_user is None or global_password is None or global_db is None:
        initialize()
        
    conn = mysql.connector.connect(
        host=global_host,
        user=global_user,
        password=global_password,
        db = global_db
    )
    drinker_list = None
    try:
        dbcursor = conn.cursor()
        dbcursor.execute(query)
        drinker_list = dbcursor.fetchall()

        dbcursor.close()
        conn.close()
    except mysql.connector.Error as e:
        return e.msg

    dbcursor.close()
    conn.close()

    return drinker_list
