import sqlite3

def startjob():
    print("Job started")
    conn = sqlite3.connect('project/db.sqlite3')
    cursor = conn.execute("SELECT * from application_users WHERE state = 'pending' AND invalid = 0;")
    for row in cursor:
        print("record = ", row)

if __name__ == '__main__':
    print("main")
    startjob()

