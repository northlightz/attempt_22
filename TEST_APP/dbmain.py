import sqlite3 #sqlite for db
import time #time for timestamps

#define db path
db_path = 'DBStored/db.db'

#define fuction to create and connect to db
def create_db():
    connect = sqlite3.connect(db_path)
    connect.execute('''CREATE TABLE IF NOT EXISTS blogs(
                    POSTER TEXT,
                    TIMESTAMP TEXT,
                    POSTTITLE TEXT,
                    POSTCONTENT TEXT);''')
    
#set global var for connect to use in later functions
connect = sqlite3.connect(db_path)

#fuction to insert data into db table
def insert_into_db(POSTER, TIMESTAMP, POSTTITLE, POSTCONTENT):
    addtodb = ('''INSERT INTO blogs (POSTER, TIMESTAMP, POSTTITLE, POSTCONTENT) VALUES (?, ?, ?, ?)''')
    connect.execute(addtodb, (POSTER, TIMESTAMP, POSTTITLE, POSTCONTENT))
    connect.commit()

#function to read from the db
def report_from_db():
    dbcursor = connect.execute('''SELECT * FROM blogs;''')
    for i in dbcursor:
        print(str(i[0])+" "+str(i[1])+" "+str(i[2])+" "+str(i[3]))
        print(str(type(i[0]))+" "+str(type(i[1]))+" " +
             str(type(i[2]))+" "+str(type(i[3]))+"\n")