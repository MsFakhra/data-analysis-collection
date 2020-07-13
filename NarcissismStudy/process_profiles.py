def checkpostdata(posts,mm,yy):
    for post in posts:
        starttuple = post
        edate = starttuple[0]
        dbdata = edate.split('-')
        yyyy = dbdata[1]
        year = yyyy[-2:]
        month = dbdata[0]
        if (year == yy and month == mm):
            return post[1]
    return 0

def checkcommentdata(comments,mm,yy):
    Analytical = 0
    Anger	= 0
    Fear	= 0
    Joy	=0
    Sadness=0
    Positive=0
    Negative=0
    Neutral=0


    for cmt in comments:
        starttuple = cmt
        edate = starttuple[0]
        dbdata = edate.split('-')
        yyyy = dbdata[1]
        year = yyyy[-2:]
        month = dbdata[0]
        if (year == yy and month == mm):
            sentiment = starttuple[3]
            count = starttuple[1]
            if sentiment == 'Positive':
                Positive = count
            else:
                if sentiment == 'Joy':
                    Joy = count
                else:
                    if sentiment == 'Neutral':
                        Neutral = count
                    else:
                        if sentiment == 'Sadness':
                            Sadness = count
                        else:
                            if sentiment == 'Negative':
                                Negative = count
                            else:
                                if sentiment == 'Confident' or sentiment == 'Tentative':
                                    Positive = Positive + count
                                else:
                                    if sentiment == 'Fear':
                                        Fear = count
                                    else:
                                        if sentiment == 'Anger':
                                            Anger = count
                                        else:
                                            if sentiment == 'Analytical':
                                                Analytical = count

    return str(Analytical) + ',' + str(Anger) + ',' + str(Fear) + ',' + str(Joy) + ',' + str(Sadness) + ',' + str(Positive) + ',' + str(Negative) + ',' + str(Neutral)

def checkpictures(instagram, pictures,mm,yy):
    otherscount = 0
    selfiecount = 0

    for picture in pictures:
        starttuple = picture
        edate = starttuple[0]
        dbdata = edate.split('-')
        yyyy = dbdata[1]
        year = yyyy[-2:]
        month = dbdata[0]
        if (year == yy and month == mm):
            if instagram == starttuple[1]:
                selfiecount = starttuple[2]
            else:
                otherscount = starttuple[2]
    return str(selfiecount) + ',' + str(otherscount)

def checklikes(likes,mm,yy):
    for like in likes:
        starttuple = like
        edate = starttuple[0]
        dbdata = edate.split('-')
        yyyy = dbdata[1]
        year = yyyy[-2:]
        month = dbdata[0]
        if (year == yy and month == mm):
            return like[1]
    return 0
def checkhashtags(hashtags,mm,yy):
    for tag in hashtags:
        starttuple = tag
        edate = starttuple[0]
        dbdata = edate.split('-')
        yyyy = dbdata[1]
        year = yyyy[-2:]
        month = dbdata[0]
        if (year == yy and month == mm):
            return tag[1]
    return 0
def write_data(instagram,posts,comments,pictures,likes,hashtags,f):
    starttuple = posts.__getitem__(0)
    edate = starttuple[0]
    endtuple = posts.__getitem__(len(posts) - 1)
    sdate = endtuple[0]
    import pandas as pd
    month_list = [i.strftime("%y-%m") for i in pd.date_range(start=sdate, end=edate, freq='MS')]

    index = len(month_list) -1
    while index >= 0:
        ddata = month_list[index].split('-')
        mm = ddata[1]
        yy = ddata[0]
        postcount = checkpostdata(posts,mm,yy)
        picturecount = checkpictures(instagram,pictures,mm,yy)
        likescount = checklikes(likes,mm,yy)
        comment = checkcommentdata(comments,mm,yy)
        htags = checkhashtags(hashtags,mm,yy)
        row = month_list[index]+ ',' + str(postcount) + ',' + picturecount + ',' + str(likescount)+ ',' +str(htags)+ ',' +comment
        f.write(row + '\n')
        index = index -1

###############################################################################################################################################################################################################

import sqlite3
conn = sqlite3.connect('project/db.sqlite3')

'''print("Opened database successfully")
res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in res:
     print(name[0])'''
i= 0
outsql = "SELECT instagram FROM application_users"
cursor = conn.execute(outsql)
for row in cursor:
    print(row)
    i +=1
print(i)

upsql = "UPDATE application_posts " \
        "SET hashtags = NULL " \
        "WHERE hashtags = 'No Hash Tag';"

cur = conn.cursor()
cur.execute(upsql)
conn.commit()


csv_result = []
list = ["fridacaarlson","saanieee"]#["nlb_.x", "lydiaajacksonx","kerry.linney"]#["emzohorne","louannvecchia","oliviameikle_"] # 'shelbymccrann','inked_keifer93','nlb_.x',
olist = ["charlotteshipman","evalouuise","kirstenmcleodd",'lisa_nolan','amelia_goodman','chloescantlebury','emilybahr','thearoberts','imymann','lisannacarmen','aribroadbent','miabrown_','slotheysimpson','lydiaajacksonx','keishahaye', 'abbiethomson__','kerry.linney','karalips','shaunaburke96']
filename = "results.csv"
firstrow = 'mm/yy' + ',' + 'Post Count' + ',' + 'Selfies,Others' + ',' + 'Avg. Likes' + ',' + 'hashtags' + ',' + 'Analytical,Anger,Fear,Joy,Sadness,Positive,Negative,Neutral'
with open(filename, "w+") as f:
    f.write(firstrow +'\n')


    for instagram in list:
        #getting id
        f.write(instagram + '\n')
        outsql = "SELECT id FROM application_users WHERE instagram = '" + instagram +"';"
        cursor = conn.execute(outsql)
        id = -1
        for row in cursor:
            id = row[0]

        ##getting data from Posts No of posts per month
        posts = []
        outsql = "SELECT strftime('%m-%Y', posted_on) as 'month-year',count(*) FROM application_posts WHERE instagram = '" + instagram +"' GROUP BY strftime('%m-%Y', posted_on) ORDER BY posted_on DESC"
        cursor = conn.execute(outsql)
        for row in cursor:
            #print("POSTS DATA = ", row)
            posts.append(row)
        ##getting comments and their sentiments
        comments = []
        outsql = "SELECT strftime('%m-%Y',application_comment.posted_on), COUNT(*),owner,sentiment,text " \
                 "FROM application_comment " \
                 "INNER JOIN application_posts on application_comment.post_id = application_posts.id WHERE owner = '" + instagram + "' " \
                 "GROUP BY strftime('%m-%Y', application_comment.posted_on), application_comment.sentiment ORDER BY application_comment.posted_on DESC;"

        #print(outsql)
        cursor = conn.execute(outsql)
        for row in cursor:
            #print("Sentiment Data = ", row)
            comments.append(row)

            ###Picture data
        pictures = []
        outsql = "SELECT strftime('%m-%Y', posted_on) as 'month-year', person,count(*) " \
                 "FROM application_picture " \
                 "WHERE instagram = " + str(id) + " GROUP BY strftime('%m-%Y', posted_on),person ORDER BY posted_on DESC;"
        #print(outsql)
        cursor = conn.execute(outsql)
        for row in cursor:
            #print("Picture Data = ", row)
            pictures.append(row)

        ###AVg number of likes
        likes = []
        outsql = "SELECT strftime('%m-%Y', posted_on) as 'month-year',avg(likes) " \
                 "FROM application_posts " \
                 "WHERE instagram = '"+instagram+"' GROUP BY strftime('%m-%Y', posted_on) ORDER BY posted_on DESC"
        cursor = conn.execute(outsql)
        for row in cursor:
            #print("Likes Data = ", row)
            likes.append(row)

        #hashtag usage
        hashtags = []
        outsql = "SELECT strftime('%m-%Y', posted_on), count(hashtags) " \
                 "FROM application_posts " \
                 "WHERE instagram = '"+ instagram +"' " \
                 "GROUP BY strftime('%m-%Y', posted_on) ORDER BY posted_on DESC"
        cursor = conn.execute(outsql)
        for row in cursor:
            #print("Hashtag Usage = ", row)
            hashtags.append(row)

        write_data(instagram,posts,comments,pictures,likes,hashtags,f)


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
