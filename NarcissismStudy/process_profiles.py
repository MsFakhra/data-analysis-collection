import sqlite3
conn = sqlite3.connect('project/db.sqlite3')

print("Opened database successfully")
res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in res:
     print(name[0])
