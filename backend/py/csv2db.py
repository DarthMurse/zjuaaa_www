import pandas as pd
import sqlite3 as sq
import math

conn = sq.connect("../db.sqlite3")
cursor = conn.cursor()

data = pd.read_csv("../other/2024.csv", header=0, dtype=str)
new_columns = ["department", "name", "student_id", "phone", "major", "dorm", "birthday", "home", "qq", "wechat", "email", "hobby", "skill", "comment"]
old_columns = ["department", "name", "student_id", "phone", "major", "birthday", "home", "qq", "email"]

def update_new(data, new_columns, conn, cursor):
    print("Emptying table app_newcontact")
    cursor.execute("delete from app_newcontact")
    print("Deleted")

    rows = len(data)
    head_str = ""
    for i in range(len(new_columns)):
        if i == 0:
            head_str += new_columns[i]
        else:
            head_str += ', ' + new_columns[i]
    #print(head_str)

    for i in range(rows):
        row = data.iloc[i]
        #print(row)
        s = ""
        for i in range(len(new_columns)):
            #print(row[new_columns[i+1]])
            if i == 0:
                s += "'%s'" % row[new_columns[i]]
            elif type(row[new_columns[i]]) == str:
                s += ", '%s'" % row[new_columns[i]]
            elif not math.isnan(row[new_columns[i]]):
                s += ", '%s'" % row[new_columns[i]]
            else:
                s += ", NULL"

        exec_str = "insert into app_newcontact (%s) values" % head_str
        s = "(" + s + ")"
        exec_str = exec_str + s
        cursor.execute(exec_str)
    conn.commit()

def update_old(old_columns, conn, cursor):
    head_str = ""
    for i in range(len(old_columns)):
        if i == 0:
            head_str += old_columns[i]
        else:
            head_str += ', ' + old_columns[i]

    cursor.execute("select %s from app_newcontact" % head_str)
    new_contact = cursor.fetchall()
    conn.commit()
    
    for item in new_contact:
        cursor.execute("select name from app_allcontact where name='%s'" % item[1])
        result = cursor.fetchall()
        conn.commit()
        # New member
        if len(result) == 0:
            s = ""
            for i in range(len(old_columns)):
                if i == 0:
                    s += "'%s'" % item[i]
                else:
                    s += ", '%s'" % item[i]
            cursor.execute("insert into app_allcontact (%s) values (%s)" % (head_str, s))
            conn.commit()
            
update_new(data, new_columns, conn, cursor)
update_old(old_columns, conn, cursor)
cursor.close()
conn.close()
# Won't work because of --secure-file-priv
'''
curosr.execute("LOAD DATA INFILE '../other/2024.csv' \
                INTO TABLE new_contact \
                FIELDS TERMINATED BY ',' \
                LINES TERMINATED BY '\n' \
                IGNORE 1 ROWS;")
conn.commit()
'''