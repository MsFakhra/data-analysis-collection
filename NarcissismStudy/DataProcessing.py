import sqlite3
conn = sqlite3.connect('project/db.sqlite3')
ALPHA = 1.2
BETA = 1.2
GAMMA = 1.2


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
def checkcommentscount(comments, mm, yy):
    commentcount = 0
    for cmt in comments:
        starttuple = cmt
        edate = starttuple[0]
        dbdata = edate.split('-')
        yyyy = dbdata[1]
        year = yyyy[-2:]
        month = dbdata[0]
        if (year == yy and month == mm):
            count = starttuple[1]
            commentcount = commentcount + count

    return commentcount

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
def checkselfiecount(instagram, pictures,mm,yy):
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
    return selfiecount

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

def get_max(instagram,posts,comments,pictures,likes,hashtags,f):
    max_posts = 0
    max_comments = 0
    max_pics = 0
    max_likes =0
    starttuple = posts.__getitem__(0)
    edate = starttuple[0]
    endtuple = posts.__getitem__(len(posts) - 1)
    sdate = endtuple[0]
    import pandas as pd
    month_list = [i.strftime("%y-%m") for i in pd.date_range(start=sdate, end=edate, freq='MS')]

    index = len(month_list) - 1
    while index >= 0:
        ddata = month_list[index].split('-')
        mm = ddata[1]
        yy = ddata[0]
        postcount = checkpostdata(posts, mm, yy)
        picturecount = checkselfiecount(instagram, pictures, mm, yy)
        likescount = checklikes(likes, mm, yy)
        commentcount = checkcommentscount(comments, mm, yy)
        if max_posts < postcount:
            max_posts = postcount
        if max_comments < commentcount:
            max_comments = commentcount
        if max_pics < int(picturecount):
            max_pics = int(picturecount)
        if max_likes < likescount:
            max_likes = likescount
        ##################
        index = index - 1
    return max_posts,max_comments,max_pics,max_likes

def compute_average(lst):
    return sum(lst) / len(lst)

def write_output_data(f,instagram,followers,npi,n_posts,n_comments,n_pics,n_likes):
    avg_n_posts     = round(compute_average(n_posts),2)
    avg_n_comments  = round(compute_average(n_comments),2)
    avg_n_pics      = round(compute_average(n_pics),2)
    avg_n_likes     = round(compute_average(n_likes),2)
    alpha = ALPHA
    beta = BETA
    gamma = GAMMA
    powered_posts = pow(avg_n_posts,alpha)
    powered_pics = pow(avg_n_pics, beta)
    powered_likes = pow(avg_n_likes, gamma)
    multiplied_value = powered_posts * powered_pics * powered_likes
    NPI_Computed = 40 * round(pow(multiplied_value, (1/(alpha+beta+gamma))),2)
    print(NPI_Computed)
    row = instagram+','+str(followers)+','+str(npi)+','+str(NPI_Computed)
    f.write(row)



def write_normalized_data(instagram,posts,comments,pictures,likes,hashtags,max_posts,max_comments,max_pics,max_likes,nf):
    n_posts = []
    n_comments = []
    n_pics = []
    nlikes = []

    starttuple = posts.__getitem__(0)
    edate = starttuple[0]
    endtuple = posts.__getitem__(len(posts) - 1)
    sdate = endtuple[0]
    import pandas as pd
    month_list = [i.strftime("%y-%m") for i in pd.date_range(start=sdate, end=edate, freq='MS')]

    index = len(month_list) - 1
    while index >= 0:
        ddata = month_list[index].split('-')
        mm = ddata[1]
        yy = ddata[0]
        postcount = checkpostdata(posts, mm, yy)
        picturecount = checkselfiecount(instagram, pictures, mm, yy)
        likescount = checklikes(likes, mm, yy)
        commentcount = checkcommentscount(comments, mm, yy)
        n_postcount = 0
        n_piccount = 0
        n_cmtscount = 0
        n_likescount = 0
        if max_posts > 0:
            n_postcount = postcount / max_posts
            n_posts.append(n_postcount)
        if max_pics > 0:
            n_piccount = int(picturecount) / max_pics
            n_pics.append(n_piccount)
        if max_comments > 0:
            n_cmtscount = commentcount / max_comments
            n_comments.append(n_cmtscount)
        if max_likes > 0:
            n_likescount = likescount / max_likes
            nlikes.append(n_likescount)
        row =  ',,'+month_list[index] + ',' + str(n_postcount) + ',' + str(n_piccount) + ',' + str(
            n_cmtscount) + ',' + str(n_likescount)
        nf.write(row + '\n')
        index = index - 1

    return n_posts, n_comments, n_pics, nlikes

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
        row = ',,'+month_list[index]+ ',' + str(postcount) + ',' + picturecount + ',' + str(likescount)+ ',' +str(htags)+ ',' +comment
        f.write(row + '\n')
        index = index -1

###############################################################################################################################################################################################################
i = 0
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
list = ["lisa_nolan"]#,"amelia_goodman","inked_keifer93","shaunaburke96","miabrown_","evalouuise","keishahaye","slotheysimpson"]#"chloescantlebury","nlb_.x","karalips","kerry.linney","abbiethomson__","aribroadbent"]#["nlb_.x", "lydiaajacksonx","kerry.linney"]#["emzohorne","louannvecchia","oliviameikle_"] # 'shelbymccrann','inked_keifer93','nlb_.x',
olist = ["charlotteshipman","evalouuise","kirstenmcleodd",'lisa_nolan','amelia_goodman','chloescantlebury','emilybahr','thearoberts','imymann','lisannacarmen','aribroadbent','miabrown_','slotheysimpson','lydiaajacksonx','keishahaye', 'abbiethomson__','kerry.linney','karalips','shaunaburke96']
#raw results
filename = "results.csv"

#normalized results between 0 - 1
normalized_file = "normalized_results.csv"
#outputfile contains the computed NPI and NPI from the questionnaire for comparison
output_file = "output.csv"
firstrow = ',,'+'mm/yy' + ',' + 'Post Count' + ',' + 'Selfies,Others' + ',' + 'Avg. Likes' + ',' + 'hashtags' + ',' + 'Analytical,Anger,Fear,Joy,Sadness,Positive,Negative,Neutral'
nf_firstrow = ',,mm/yy,posts_count,pic_count,comments_count,likes_count'
out_firstrow = ',,NPI_Recieved, NPI_Computed'
with open(filename, "w+") as f, open(normalized_file, "w+") as nf, open(output_file, "w+") as of :
#with open(filename, "w+") as f:
    f.write(firstrow +'\n')
    nf.write(nf_firstrow +'\n')
    of.write(out_firstrow + '\n')

    for instagram in list:
        #getting id
        print(instagram)
        outsql = "SELECT id,followers,npi_score FROM application_users WHERE instagram = '" + instagram +"';"
        cursor = conn.execute(outsql)
        id = -1
        followers = -1
        for row in cursor:
            id = row[0]
            followers = row[1]
            npi = row[2]
        f.write(instagram + ',' + str(followers) + '\n')
        nf.write(instagram + ',' + str(followers) + '\n')
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
        max_posts,max_comments,max_pics,max_likes = get_max(instagram,posts,comments,pictures,likes,hashtags,f)
        write_data(instagram,posts,comments,pictures,likes,hashtags,f)
        n_posts,n_comments,n_pics,n_likes = write_normalized_data(instagram,posts,comments,pictures,likes,hashtags,max_posts,max_comments,max_pics,max_likes,nf)
        write_output_data(of,instagram,followers,npi,n_posts,n_comments,n_pics,n_likes)
exit(0)

#pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f