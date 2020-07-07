import sqlite3
conn = sqlite3.connect('project/db.sqlite3')

'''print("Opened database successfully")
res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in res:
     print(name[0])'''

upsql = "UPDATE application_posts " \
        "SET hashtags = NULL " \
        "WHERE hashtags = 'No Hash Tag';"
list = ["lisa_nolan"]#, "amelia_goodman","diipakhosla","chloescantlebury","emilybahr","thearoberts","imymann"]

for instagram in list:
    #getting id
    outsql = "SELECT id FROM application_users WHERE instagram = '" + instagram +"';"
    cursor = conn.execute(outsql)
    id = -1
    for row in cursor:
        id = row[0]

    ##getting data from Posts No of posts per month
    outsql = "SELECT count(*),strftime('%m-%Y', posted_on) as 'month-year' FROM application_posts WHERE instagram = '" + instagram +"' GROUP BY strftime('%m-%Y', posted_on) ORDER BY posted_on"
    cursor = conn.execute(outsql)
    for row in cursor:
        print("POSTS DATA = ", row)
    ##getting comments and their sentiments
    outsql = "SELECT COUNT(*),owner,sentiment,strftime('%m-%Y',application_comment.posted_on),text " \
             "FROM application_comment " \
             "INNER JOIN application_posts on application_comment.post_id = application_posts.id WHERE instagram = '" + instagram + "' " \
             "GROUP BY strftime('%m-%Y', application_comment.posted_on), application_comment.sentiment ORDER BY application_comment.posted_on;"

    print(outsql)
    cursor = conn.execute(outsql)
    for row in cursor:
        print("Sentiment Data = ", row)

        ###Picture data
    outsql = "SELECT count(*),person,strftime('%m-%Y', posted_on) as 'month-year' " \
             "FROM application_picture " \
             "WHERE instagram = " + str(id) + " GROUP BY strftime('%m-%Y', posted_on),person ORDER BY posted_on;"
    print(outsql)
    cursor = conn.execute(outsql)
    for row in cursor:
        print("Picture Data = ", row)

    ###AVg number of likes
    outsql = "SELECT avg(likes),strftime('%m-%Y', posted_on) as 'month-year' " \
             "FROM application_posts " \
             "WHERE instagram = '"+instagram+"' GROUP BY strftime('%m-%Y', posted_on) ORDER BY posted_on"
    cursor = conn.execute(outsql)
    for row in cursor:
        print("Likes Data = ", row)

    #hashtag usage
    outsql = "SELECT posted_on, count(hashtags) " \
             "FROM application_posts " \
             "WHERE instagram = '"+ instagram +"' " \
             "GROUP BY strftime('%m-%Y', posted_on) ORDER BY posted_on"
    cursor = conn.execute(outsql)
    for row in cursor:
        print("Hashtag Usage = ", row)

exit(0)


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

'''insql = "INSERT INTO application_picture (instagram,posted_on,selfie,person,image_path ) VALUES ('%s','%s','False','Others','usmanmaliktest/2020-05-26_10-12-54_UTC_1.jpg')"\
        %(profile,datetime_obj)

print(insql)
conn.execute(insql)
conn.commit()'''




from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
#ref: https://www.codetable.net/unicodecharacters?page=89
happy = [128513,128514,128515,128516,128517,128518,128519,128520,128521,128522,128523,128524
    ,128525,128526,128536,128538,128540,128541,128568,128569,128570,128571,128572 ,128573
    ,128584,128585,128586 #cats
    ,128587,128588,128591 #monkeys
    ,10084,10083,10085,10086,10087 #black hearts
    ,128293,128076,128079
    ]
neutral = [128527,128528,128530,128554,128555,128562,128563,128565,128566,128567,128582
    ,128070,128071,128072,128073]
anxiety = [128531,128532,128534]
angry = [128542,128544,128545,128574,128581,128589,128590]
sad = [128546,128547,128548,128549,128553,128557,128560,128575,128576,128078]
fear = [128552,128561]

def checkemoji(text):
    for ch in text:
       ord_value = ord(ch)
       if(happy.__contains__(ord_value)):
            return "Joy",0.8
       else:
            if (neutral.__contains__(ord_value)):
                return "Neutral",0.0
            else:
                if (anxiety.__contains__(ord_value)):
                    return "Anxiety",-0.1
                else:
                    if (angry.__contains__(ord_value)):
                        return "Angry",-0.8
                    else:
                        if (sad.__contains__(ord_value)):
                            return "Sad",-0.4
                        else:
                            if (fear.__contains__(ord_value)):
                                return "Tentative",0.0
    return "no_emoji",0.0
def vader_tone(text):
    vs = analyzer.polarity_scores(text)
    score = vs['compound']
    if (score >= 0.05):
        tone_name = "Positive"
    else:
        if (score > -0.05 and score < 0.05):
            tone_name, score = checkemoji(text)
        else:
            if (score <= -0.05):
                tone_name = "Negative"
    return tone_name,score

#text = '@mahee2000 fierce as fuck 🔥'
text = 'fuck i love you'

if(text.__contains__('fuck')):
    text = text.replace('fuck', '')
if(text.__contains__('fierce')):
    tone_name, score = checkemoji(text)
    if(tone_name == "no_emoji"):
        tone_name,score = vader_tone(text)
else:
    tone_name,score = vader_tone(text)
print(tone_name + str(score))
