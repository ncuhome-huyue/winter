from sqlite3 import *

conn = connect('pinglun.db')
c = conn.cursor()
c.execute('''CREATE TABLE COMPANY
       (pl_id       TEXT    NOT NULL,
       pl           TEXT     NOT NULL,
       bookID       TEXT    NOT NULL,
       bookname      TEXT    NOT NULL,
       fromID       TEXT    NOT NULL,
       time         TEXT    NOT NULL,
       zan          INT     NOT NULL,
       cai          INT     NOT NULL);''')
conn.commit()
conn.close()

conn = connect('zan_and_cai.db')
c = conn.cursor()
c.execute('''CREATE TABLE COMPANY
       (pl_id       TEXT    NOT NULL,
       kind         TEXT    NOT NULL,
       bookID       TEXT    NOT NULL,
       fromID       TEXT    NOT NULL,
       time         TEXT    NOT NULL);''')
conn.commit()
conn.close()

conn = connect('collection.db')
c = conn.cursor()
c.execute('''CREATE TABLE COMPANY
       (bookID       TEXT    NOT NULL,
       bookname      TEXT    NOT NULL,
       usernameID       TEXT    NOT NULL);''')
conn.commit()
conn.close()
