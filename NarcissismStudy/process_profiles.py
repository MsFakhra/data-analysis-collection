import sqlite3
conn = sqlite3.connect('project/db.sqlite3')

print("Opened database successfully")
res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in res:
     print(name[0])

'''cursor = conn.execute("SELECT ID from application_posts")
for row in cursor:
   print("ID = ", row[0])
'''

x = 51
bio = 'hello'
profile = 'usmanmaliktest'
from datetime import datetime
date1 = datetime.today().strftime('%m-%d-%y') #2020-06-03

date1 = datetime.today()
date = date1.strftime('"%y/%m/%d"')

date_str = '31-12-2017' # The date - 29 Dec 2017
format_str = '%d-%m-%Y' # The format
datetime_obj = datetime.strptime(date_str, format_str)
date = datetime_obj.strftime('"%y/%m/%d"')


date_str = '2018-12-17' # The date - 29 Dec 2017
format_str = '%Y-%m-%d' # The format
datetime_obj = datetime.strptime(date_str, format_str)
date = datetime_obj.strftime('"%y/%m/%d"')



#insql = "INSERT INTO application_users (instagram,full_name,email,selfie,npi_score,biography,media_count,followers,following,created_at,state) VALUES ('%s','%s','fakhraikram@yahoo.com','Null','%d','Test Account',%d,%d,%d,'1980-11-07','pending')"%('usmanmaliktest','Test Account',-1,-1,-1,-1)


insql = "INSERT INTO application_users (instagram,full_name,email,selfie,npi_score,biography,media_count,followers,following,created_at,state) " \
        "VALUES ('%s','%s','fakhraikram@yahoo.com','Null','%d','Test Account',%d,%d,%d,%s,'pending')"\
        %(profile,'Test Account',-1,-1,-1,-1,date)

insql = "INSERT INTO application_posts (user_id,instagram,posted_on,post_url,hashtags,mentions,tagged_users,is_video,likes,caption ) VALUES ('31','usmanmaliktest','20/05/26','https://scontent-amt2-1.cdninstagram.com/v/t51.2885-15/e35/100950436_284088066164778_7273162332394211336_n.jpg?_nc_ht=scontent-amt2-1.cdninstagram.com&_nc_cat=106&_nc_ohc=azeHcl5Uj-0AX-c8fXj&oh=54a04deefbee7c2a94d54a89c6c6172c&oe=5F1C63B2','#stay_safe_keep_safe #takecare','[]','@doctor_corona','False','1','Test post')"

insql = "INSERT INTO application_picture (instagram,posted_on,selfie,person,image_path ) VALUES ('31','20/05/26','False','Others','usmanmaliktest/2020-05-26_10-12-54_UTC_1.jpg')"

print(insql)
conn.execute(insql)
conn.commit()
#conn.close()



#date2 = datetime.date(2018, 1, 4)
#UPDATION WITH THIS
'''profile = "test3"
sql = "UPDATE application_users SET biography = 'hello', media_count = 190,followers = 110,following = 10 WHERE instagram ='" + profile + "';"
cur = conn.cursor()
cur.execute(sql)
conn.commit()'''

##SELECTION WITH THIS
'''cursor = conn.execute("SELECT * from application_users WHERE instagram ='" + profile + "';")
for row in cursor:
    print("ID = ", row)
'''

####Extraction w.r.t. Date
cursor = conn.execute("SELECT * from application_users WHERE created_at >" + date + ";")
for row in cursor:
    print("application_users ID = ", row)

print (date)
#OR
####Extraction w.r.t. Date
query = "SELECT * from application_comment WHERE posted_on >'" + date + "';" #differce of ''
print(query)
cursor = conn.execute(query)
for row in cursor:
    print("ID = ", row)


# select users which are not processed
# in a loop . apply face recoginition on user
# get score
# get instagram profile , and photos
# do you magic
# update database




conn.close()