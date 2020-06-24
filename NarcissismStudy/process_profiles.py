import sqlite3
conn = sqlite3.connect('project/db.sqlite3')

print("Opened database successfully")

# res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
# for name in res:
#     print(name[0])
#

cursor = conn.execute("SELECT id from application_users")
for row in cursor:
   print("ID = ", row[0])


# select users which are not processed
# in a loop . apply face recoginition on user
# get score
# get instagram profile , and photos
# do you magic
# update database




conn.close()