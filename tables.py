import sqlite3
from datetime import datetime
conn =sqlite3.connect('database/vasudev_hospital.db')
cur = conn.cursor()
# cur.execute('CREATE TABLE userdata( userid INTEGER PRIMARY KEY AUTOINCREMENT,\
#     fname TEXT,lname TEXT,email TEXT,age INTEGER,phonenumber INTEGER,\
#         password TEXT,city TEXT,gender TEXT);')
# cur.execute(' DROP TABLE userdata;')


'''cur.execute('CREATE TABLE appointment(appointment_id INTEGER PRIMARY KEY AUTOINCREMENT\
    ,date date ,time TEXT,\
    userid INTEGER,FOREIGN KEY (userid) REFERENCES userdata(userid));')'''


'''# cur.execute('CREATE TABLE to_do_list(id INTEGER PRIMARY KEY AUTOINCREMENT,taskname text,end_date text,end_time text);')
records=cur.execute('select * from to_do_list;').fetchall()'''

conn.commit()

conn.close()