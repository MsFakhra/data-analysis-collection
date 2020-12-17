import sqlite3

conn = sqlite3.connect('project/db.sqlite3')


def extract_information(id):
    print("Extracting Information")
    cursor = conn.execute("SELECT instagram from application_users WHERE id =" + str(id) + ";")
    for row in cursor:
        profilename = row[0]
    print(profilename)

def startjob():
    print("Job started")
    cursor = conn.execute("SELECT * from application_users WHERE state = 'pending' AND invalid = 0;")
    for row in cursor:
        id = row[0]
        extract_information(id)

if __name__ == '__main__':
    print("main")
    startjob()

