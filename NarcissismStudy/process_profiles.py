##Latest code for profile analysis updated in 21st July 2020
import pickle

from instaloader import Instaloader, Profile
from datetime import datetime
import itertools
from itertools import dropwhile, takewhile
import time
from math import sqrt
from sklearn import neighbors
from os import listdir
from os.path import isdir, join, isfile, splitext
import face_recognition
from face_recognition import face_locations
from face_recognition.cli import image_files_in_folder
#from face_recognition.face_detection_cli import image_files_in_folder

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import sqlite3

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#######initializations
#Tone Analysis
from watson_developer_cloud import ToneAnalyzerV3
apikey = 'Sst3Vq2D221Alx-YbgLNtwOyu5fywKtaL2rl8NSl9-m3'#'wGySQLw3nxEOhEirYSvAZScum9v_1_VoA8lKZYMi6ip-'
urlref = 'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/2ba5653f-b626-495a-9efc-c9e3f6428c59'#'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/618c6917-36fa-4dd7-a10b-8df2ed184446'
version = '2/25/2020'#'2020-02-20'#'2020-02-21'


vanalyzer = SentimentIntensityAnalyzer()
#Prereqs
# Text
def initializeAnalyzer():
    # we imported time because ToneAnalyzer versions have YYYY-MM-DD format
    currentVersion = time.strftime("%Y-%m-%d")
    print_string = "Using Tone Analyzer\'s version: " + str(currentVersion)
    print("=" * len(print_string))
    print( print_string)
    print ("=" * len(print_string))
    tone_analyzer3 = ToneAnalyzerV3(
            version=currentVersion,
            iam_apikey=apikey,
            url=urlref
    )
    return tone_analyzer3

#Images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def train(train_dir, model_save_path = "", n_neighbors = None, knn_algo = 'ball_tree', verbose=False):
    """
    Trains a k-nearest neighbors classifier for face recognition.

    :param train_dir: directory that contains a sub-directory for each known person, with its name.

     (View in source code to see train_dir example tree structure)

     Structure:
        <train_dir>/
        ├── <person1>/
        │   ├── <somename1>.jpeg
        │   ├── <somename2>.jpeg
        │   ├── ...
        ├── <person2>/
        │   ├── <somename1>.jpeg
        │   └── <somename2>.jpeg
        └── ...
    :param model_save_path: (optional) path to save model of disk
    :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified.
    :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
    :param verbose: verbosity of training
    :return: returns knn classifier that was trained on the given data.
    """
    X = []
    y = []
    for class_dir in listdir(train_dir):
        if not isdir(join(train_dir, class_dir)):
            continue
        for img_path in image_files_in_folder(join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            faces_bboxes = face_locations(image)
            if len(faces_bboxes) != 1:
                if verbose:
                    print("image {} not fit for training: {}".format(img_path, "didn't find a face" if len(faces_bboxes) < 1 else "found more than one face"))
                continue
            X.append(face_recognition.face_encodings(image, known_face_locations=faces_bboxes)[0])
            y.append(class_dir)


    if n_neighbors is None:
        n_neighbors = int(round(sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically as:", n_neighbors)

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    if model_save_path != "":
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)
    return knn_clf

##Email
MY_ADDRESS = 'behavioralstats@outlook.com'
PASSWORD = 'Amsterdam1234'


#ref: https://www.codetable.net/unicodecharacters?page=89
#ref: https://www.codetable.net/unicodecharacters?page=89
happy = [128513,128514,128515,128516,128517,128518,128519,128520,128521,128522,128523,128524
    ,128525,128526,128536,128538,128540,128541,128568,128569,128570,128571,128572 ,128573
    ,128584,128585,128586 #cats
    ,128587,128588,128591 #monkeys
    ,10084,10083,10085,10086,10087 #black hearts
    ,128293,128076,128079,128077
    ]
neutral = [128527,128528,128530,128554,128555,128562,128563,128565,128566,128567,128582
    ,128070,128071,128072,128073]
anxiety = [128531,128532,128534]
angry = [128542,128544,128545,128574,128581,128589,128590]
sad = [128546,128547,128548,128549,128553,128557,128560,128575,128576,128078]
fear = [128552,128561]

L = Instaloader()
analyzer = initializeAnalyzer()  #sentiment analyzer
knn_clf = train('project/application/static/media') #image knn classifier
conn = sqlite3.connect('project/db.sqlite3') #Database
#print("Opened database successfully")

#exit(0)
#######initializations
class TextScore(object):
    def __init__(self, tone,score):
        self.tone = tone
        self.score = score
class Message:
    index = 0
    likes = 0
    def __init__(self,iscomment, msg,ownedby,tstamp):
        self.iscomment = iscomment;
        self.message = msg;
        self.sentiment = "Neutral";
        self.owner = ownedby;
        self.timestamp = tstamp;
        self.compscore = 0.0;
        self.is_tag_used = False
        self.authorship = ''
    def setEmotion(self,tone_score):
        self.sentiment = tone_score.tone;
        self.compscore = tone_score.score
    def setLikes(self,likes):
        self.likes = likes;
    def setIndex(self,index):
        self.index = index;
    def set_authorusestags(self,tags):
        self.is_tag_used = tags
    def setAuthorship(self,isauthor):
        self.authorship = isauthor


'''#one post usmanmaliktest
SINCE = datetime(2020, 5, 1)    #yyyy-mm-dd
UNTIL = datetime(2020,6,1)
'''
#all posts in duration
#Final
SINCE = datetime(2018, 8, 1)    #yyyy-mm-dd 2020-05-30 2019-08-05
UNTIL = datetime(2019, 12, 31)    #yyyy-mm-dd 2020-05-30
#Debugging
#SINCE = datetime(2018, 8, 5)    #yyyy-mm-dd 18/10/18
#UNTIL = datetime(2018, 8, 7)    #yyyy-mm-dd 2020-05-30
def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
def send_email(id):
    if (id == -1):
        return
    outsql = "SELECT * FROM application_users WHERE id =" + str(id) + ";"
    cursor = conn.execute(outsql)
    for row in cursor:
        email = row[2]
        name = row[1]
        if name is None or email is None:
            return
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp-mail.outlook.com',
                     port=587)  # smtplib.SMTP(host='your_host_address_here', port=your_port_here)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()  # create a message

    message = message_template.substitute(PERSON_NAME=name.title(), ID = id)

    # Prints out the message body for our sake
    print(message)

    # setup the parameters of the message
    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Results are ready"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()

def extract_information(id):
    # here create the basic model for user info; NPI is not here
    # path is image path
    cursor = conn.execute("SELECT instagram from application_users WHERE id =" + str(id) + ";")
    for row in cursor:
        profilename = row[0]

    profilepath = profilename  # Obtain profile
    profile = Profile.from_username(L.context, profilename)
    followers = profile.followers
    full_name = profile.full_name
    biography = profile.biography
    media_count = profile.mediacount
    followees = profile.followees
    not_public = profile.is_private

    if (not_public):
        private = 1
    else:
        private = 0

    # Updating user table with information
    upsql = "UPDATE application_users SET " \
            "full_name = '" + full_name + "'," \
            "biography = '" + biography + "'," \
            "media_count = " + str(media_count) + "," \
            "followers = " + str(followers) + "," \
            "following = " + str(followees) + "," \
            "public = " + str(private) + "," \
            "state = '" + 'processing' + "' WHERE id =" + str(id) + ";"
    print(upsql)
    cur = conn.cursor()
    cur.execute(upsql)
    conn.commit()

    if (private):
        upsql = "UPDATE application_users SET " \
                "biography = '" + biography + "'," \
                "media_count = " + str(media_count) + "," \
                "followers = " + str(followers) + "," \
                "following = " + str(followees) + "," \
                "private = '" + str(private) + "'," \
                "state = '" + 'processed' + "' WHERE id =" + str(id) + ";"
        print(upsql)
        cur = conn.cursor()
        cur.execute(upsql)
        conn.commit()

        send_email(id)
    else:
        upsql = "UPDATE application_users SET " \
                "biography = '" + biography + "'," \
                "media_count = " + str(media_count) + "," \
                "followers = " + str(followers) + "," \
                "following = " + str(followees) + "," \
                "private = '" + str(private) + "'," \
                "state = '" + 'processing' + "' WHERE id =" + str(id) + ";"
        print(upsql)
        cur = conn.cursor()
        cur.execute(upsql)
        conn.commit()

    image_processed = False
    posts_processed = False
    posts = extract_posts(profile, profilepath)
    print("posts extracted")
    posts_processed = process_posts(posts, profilename, id)
    print(posts_processed)

    ########## Image Processing ###########
    # Here check if record is already in DB then no need to train for images then
    # model_save_path = "./model/model.txt"
    # knn_clf = train('TrainingDataset',model_save_path)

    if (posts):
        image_processed = process_Images(profilename, id)  # ,model_save_path)
        print("images processed")
    else:
        image_processed == True
    if posts_processed == True and image_processed == True:
        upsql = "UPDATE application_users SET state = '" + 'processed' + "' WHERE id =" + str(id) + ";"
        cur = conn.cursor()
        cur.execute(upsql)
        conn.commit()
        send_email(id)

    print(profilename + "complete and id" + id)
    return private


def extract_posts(profile,profilepath):
    # Obtain posts sorted w.r.t date
    '''
    :param profile: the profile name
    :param profilepath:
    :return: list containing posts extracted
    '''
    posts = []
    posts_sorted_by_date = sorted(profile.get_posts(), key=lambda p: p.date, reverse=False)
    counter = 0
    #for post in takewhile(lambda p: p.date <= UNTIL, dropwhile(lambda p: p.date <  SINCE, posts_sorted_by_date)):
    for post in posts_sorted_by_date:
        #print (post.caption)
        if not post.is_video:
            json = L.download_post(post,profilepath)
        posts.append(post)
        counter += 1
        print(counter)
    #print(len(posts_sorted_by_date))
    return posts

######################### Tone Analysis

def process_posts(posts,profilename,user_id):
    '''
    This function process the post data and fill into the database
    :param posts:
    :param profilename:
    :return: boolean that post is processsed
    '''
    instagram = profilename
    processed = False
    cmtlist = []
    hashtaglist = []
    for post in posts:
        processed = False
        caption = post.caption
        #if(caption.__contains__("Vaada kar ke gayi si aitvaar da but it’s bank holiday tmr")):
        #    x = 10
        if caption is None:
            caption = 'No caption'
        else:
            if (caption.__contains__("'")):
                import re
                caption = re.sub('[^a-zA-Z0-9 \n\.]', '', caption)
        ##### priliminary information #####
        datetime_object = post.date #datetime
        posted_on = datetime_object.strftime('"%y/%m/%d"')
        post_url = post.url #str
         #str
        is_video = post.is_video #bool
        likes = post.likes #int
        ##### ##### #####
        #process mentions and hashtags
        mentions = process_mentions(post)
        hashtags = process_caption_tags(post) #str
        #print(hashtags)

        #taggedusers
        tagged_users = process_tagged_users(post) #str
        #print(tagged_users)

        ##Inserting a post to database
        insql = "INSERT INTO application_posts (user_id,instagram,posted_on,post_url,hashtags,mentions,tagged_users,is_video,likes,caption ) " \
                "VALUES ('%d','%s','%s','%s','%s','%s','%s','%s','%d','%s')" \
                % (user_id,instagram,datetime_object,post_url,hashtags,mentions,tagged_users,is_video,likes,caption)
        print(insql)
        conn.execute(insql)
        conn.commit()
        #process comments
        if(post.comments > 0):
            cmtlist = process_comments(post,profilename)
            if(cmtlist):
                id = -1
                outsql = "SELECT ID from application_posts WHERE post_url = '" + post_url + "';"
                cursor = conn.execute(outsql)
                for row in cursor:
                    id = row[0]
                processed = write_comments_db(cmtlist, profilename,id)
            else:
                print("No conversations found in "+insql)
                processed = True
    #print('should update posts in db and then update processed as true')
    return processed;
            #save this in database
#write Comments to DB
def write_comments_db(cmtlist, profilename,post_id):
    processed = False
    message = cmtlist[0]
    datetime_object = message.timestamp
    posted_on = message.timestamp.strftime('"%y/%m/%d"')
    owner = message.owner
    is_comment = message.iscomment
    sentiment = message.sentiment
    sscore = message.compscore
    tag_used = message.is_tag_used
    likes = message.likes
    text = message.message
    if (text.__contains__("'")):
        import re
        text = re.sub('[^a-zA-Z0-9 \n\.]', '', text)
    insql = "INSERT INTO application_comment (post_id,posted_on,owner,is_comment,sentiment,sscore,tag_used,likes,text) " \
                    "VALUES ('%d','%s','%s','%s','%s','%f','%s','%d','%s')" \
                    %(post_id,datetime_object,owner,is_comment,sentiment,sscore,tag_used,likes,text)
    print(insql)
    conn.execute(insql)
    conn.commit()
    reply_list = cmtlist[1]
    index = 0
    processed = True
    while index < len(reply_list):
        processed = False
        reply = reply_list[index]
        datetime_object = reply.timestamp
        posted_on = reply.timestamp.strftime('"%y/%m/%d"')
        owner = reply.owner
        is_comment = reply.iscomment
        sentiment = reply.sentiment
        sscore = reply.compscore
        tag_used = reply.is_tag_used
        likes = reply.likes
        text = reply.message
        if (text.__contains__("'")):
            import re
            text = re.sub('[^a-zA-Z0-9 \n\.]', '', text)
        insql = "INSERT INTO application_comment (post_id,posted_on,owner,is_comment,sentiment,sscore,tag_used,likes,text) " \
                "VALUES ('%d','%s','%s','%s','%s','%f','%s','%d','%s')" \
                % (post_id, datetime_object, owner, is_comment, sentiment, sscore, tag_used, likes, text)

        print(insql)
        conn.execute(insql)
        conn.commit()
        processed = True
        index += 1
    return processed
##Process mentions
def process_mentions(post):
    mentions = post.caption_mentions
    if len(mentions) == 0:
        return "No mentions"
    else:
        mentions_list = '\n'.join(mentions)
        return mentions_list

##Process Tagged Users
def process_tagged_users(post):
    hashtags = post.tagged_users
    if len(hashtags) == 0:
        return "No Tagged User"
    else:
        tags_list = '@'+ '@'.join(hashtags)
        return tags_list
##Process Hashtags
def process_caption_tags(post):
    hashtags = post.caption_hashtags
    if len(hashtags) == 0:
        return "No Hash Tag"
    else:
        tags_list = '#' + ' #'.join(hashtags)
        return tags_list
##Process Comments
def process_comments(post,profilename):
    cmtlist = [];
    comments = post.get_comments()
    ###processing comments
    for cmt in comments:
        comment = cmt.text.replace('\n', ' ').replace('\r', '');
        stamp = cmt.created_at_utc;
        msg = Message(True, comment, cmt.owner.username, stamp);
        ############# analyzing comment for like ... a narcisst will prefer to like his praise
        answer = cmt.answers
        ####Observing likes
        like_count = 0;
        import inspect2
        dict = inspect2.getgeneratorlocals(answer)
        items = dict.items();
        for p_id, p_info in items:
            # print("\nNode ID:", p_id)
            if (p_id == 'node'):
                for key in p_info:
                    # print(key + ':', p_info[key])
                    if (key == 'edge_liked_by'):
                        field = p_info[key]
                        like_count = field['count']
        msg.setLikes(like_count);

        ############################ Conversation if present otherwise ignore

        reply_no = 0
        pca = cmt.answers
        influencerinvolved = False
        replyList = [];
        for r in pca:
            reply = r.text;
            name = r.owner.username
            if (name == profilename):
                influencerinvolved = True
            reply = reply.replace('\n', ' ').replace('\r', '');
            stamp = r.created_at_utc  # .created_at_utc.isoformat();
            replymsg = Message(False, reply, name, stamp);
            is_tag_used = Taggedcomment(reply)
            if (name == profilename and is_tag_used == True):
                replymsg.set_authorusestags(is_tag_used);
            reply_no = reply_no + 1;
            replymsg.setIndex(reply_no)
            if (name == profilename):
                replymsg.setAuthorship('True')
            replyList.append(replymsg);
        if influencerinvolved:
            convlist = [msg]
            convlist.append(replyList)
            process_conversations_emotions(convlist)
            return convlist
    print ("cmtlist:" , cmtlist)
    return cmtlist;

def extractTone(dict_element):
    text = dict_element.get('text')
    sentiment = dict_element.get('tone_name')
    score = dict_element.get('score')
    return text,score,sentiment
def process_as_list(result,convlist):
    ########### each message is a conversation here
    # fill tones in emotions
    comment = convlist[0]
    tone_analysis = result[0].pop();
    text, score, sentiment = extractTone(tone_analysis)
    if (text and score == -1000):
        comment.sentiment = "Neutral"
        comment.compscore = 0.0
    else:
        comment.sentiment = sentiment
        comment.compscore = score

    i = 1;
    while i < len(result):
        tone_analysis = result[i].pop()
        # tone_analysis = convlist[i]
        text, score, sentiment = extractTone(tone_analysis)
        reply = convlist[1][i - 1]
        if (text and score == -1000):
            reply.sentiment = "Neutral"
            reply.compscore = 0.0
        else:
            reply.sentiment = sentiment
            reply.compscore = score
        i += 1

def process_as_dict(result,convlist):
    ########### This function makes conversation (using multi sentences in a message)

    # making one message
    removeitem = [{
        'text': "<br>.",
        'score': -1000,
        'tone_name': ''}]
    newline = False
    index = 0;
    length = len(result)
    sentences = []
    sentence = []
    while (index < length):
        item = result[index]
        if index == 5:
            x = 10
        if (item[0].get('text').__contains__("<br>")):
                newline = True
                if sentence:
                    sentences.append(sentence)
                    sentence = []
                    newline = False
                value = item[0].get('text').replace("<br>.", "")
                if value != '':
                    value = item.pop(0)
                    sentence.append(value)
        else:
                value = item.pop(0)
                sentence.append(value)

        if newline:
                sentences.append(sentence)
                sentence = []
                newline = False
        index += 1
    sentences.append(sentence)
    # Analytical	Anger	Fear	Joy	Sadness	Tentative	Confident	Positive	Negative	Neutral
    Emotions = ['Anger', 'Fear', 'Joy', 'Sadness', 'Disgust']

    ########### making conversation
    #extracting one emotion for a conversation
    conversation = []

    for msg in sentences:
        msgslist = msg
        message_result = {'text': '', 'tone_name': '', 'score': 0}
        if(msgslist):
            message = msgslist[0];
            message_result['score'] = message.get('score')
            message_result['tone_name'] = message.get('tone_name')
            message_result['text'] = message.get('text')
            index = 1   #get replies
            while index < len(msgslist):
                dic = msgslist[index];
                # merger multiple sentences
                if (dic['tone_name'] in Emotions):
                    message_result['score'] = dic['score']
                    message_result['tone_name'] = dic['tone_name']
                message = {'text': message.get('text', ' ') + dic['text']}
                #message_result['text'] = message['text']
                message_result.update(message)
                index += 1
        conversation.append(message_result)


    ##################################
    #fill tones in emotions
    comment = convlist[0]
    tone_analysis = conversation[0];
    text,score,sentiment = extractTone(tone_analysis)
    if (text and score == -1000):
        comment.sentiment = "Neutral"
        comment.compscore = 0.0
    else:
        comment.sentiment = sentiment
        comment.compscore = score

    i = 0;
    if len(convlist) > 1:
        replies = convlist[1]
        for reply in replies:
            tone_analysis = conversation[i+1]
            text,score,sentiment = extractTone(tone_analysis)
            if(text and score == -1000):
                reply.sentiment = "Neutral"
                reply.compscore = 0.0
            else:
                reply.sentiment = sentiment
                reply.compscore = score
            i += 1
def process_text(text):
    import re
    mention_regex = re.compile(r"(?:@)(\w(?:(?:\w|(?:\.(?!\.))){0,28}(?:\w))?)")
    item = re.findall(mention_regex, text.lower())
    str = text
    for i in item:
        str = str.replace(i, "")
    return str.replace("@", "")


def process_conversations_emotions(convlist):
    #INPUT: convlist contain messages with author details
    #OUTPT: convlist with emotions
    import re
    message = convlist[0]
    text = message.message
    if(text.__contains__("@")):
        text = process_text(text)
    #making single conversation => saving API calls
    #conv = message.message + ". <br>. "
    conv = text + ". <br>. "
    replies = convlist[1]
    ch = ''
    for reply in replies:
        #print(reply.message)
        text = reply.message
        if (text.__contains__('@')):
            text = process_text(text)
        val = text.strip()
        if text and val:
                ch = text[-1]
        else:
            text = "I am neutral"
        if(ch == '.'):#eliminating last fullstop
            text = text[0:text.__len__() - 1]
        conv = conv + text + ". <br>. "
        #conv = conv + reply.message + ". <br>. "
    takelastout = len(conv)- 6
    conv = conv[0:takelastout]
    result = processTexts(conv)

    ##############iteration of results
    if(len(convlist) == len(result)):
        process_as_list(result,convlist)
    else:
        process_as_dict(result,convlist)

def Taggedcomment(text):
    hindex = -1;
    hindex = text.find('#')
    if(hindex > -1):
        return True;
    else:
        return False;

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
    return "no_emoji",-1000

def vader_tone(text):
    vs = vanalyzer.polarity_scores(text)
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

def extract_tone_correspondence(sentence):
    phrase = ''
    tone_name = ''
    score = -1000


    for key, value in sentence.items():
        if(key == 'text'):
            phrase = value
        if(key == 'tones'):
            tone_list = value
            for item in tone_list:
              tone_name = item.pop('tone_name')
              score = item.pop('score')
    if tone_name == 'Tentative':
        tone_name, score = checkemoji(phrase)
    if (phrase.__contains__('fuck')):
        text = phrase.replace('fuck', '')
        tone, sscore = vader_tone(text)
        #tone2,score2 = checkemoji(text)
        if (sscore > -0.05):
            tone_name = 'Joy'
            score = 0.8
    if (phrase.__contains__('fierce')):
        tone_name, score = checkemoji(phrase)
    if (score == -1000 or tone_name == 'Analytical'):
        tone_name, score = vader_tone(phrase)
    jsonobject = [{
        "text": phrase,
        "tone_name" : tone_name,
        "score": score
    }]


    return jsonobject;

def processTexts(text):
    # INPUT: process multiple texts seperated by .<br>.
    # OUTPUT: return dictionary containing score of all sentences with score. Sentences seperated by '.' or .<br>.
    result = []
    tone_analysis = analyzer.tone({'text': text}, content_type='application/json').get_result()

    for key, value in tone_analysis.items():
        key_value = key
        if(key_value == 'sentences_tone'):
            sentences_list = value #dict
            for sentence in sentences_list:
                jsoncorrespondance = extract_tone_correspondence(sentence)
                result.append(jsoncorrespondance)
    return result

##########################Tone Analysis end

###########Image Analysis

def extract_date(img_path):
    data = img_path.split('.')
    date_data = data[0]
    date_data = date_data.split('_UTC')
    date_data = date_data[0].split('_')
    return date_data[0]

def process_Images(profilename,instagram):#,model_save_path):
    #takes the profile folder and uses knn to identify faces
    #returns list of selfies of the profile
    image_details_list = []
    predictionfolder = profilename
    print("predicting")
    predcount = 0
    for img_path in listdir(predictionfolder):
        preds = predict(join(predictionfolder, img_path) ,knn_clf=knn_clf)#,model_save_path = model_save_path)
        #print("preds: ",preds)
        valid = preds[0]
        precount = 0
        found = False
        if(valid != 'Invalid'):
            for pred in preds:
               #location = pred[1] location of face
               #print("pred: ", pred)
               date = extract_date(img_path)

               if(len(preds) > 1):
                   precount += 1
                   #for imagetuple in preds:
                   if profilename in pred:#imagetuple:
                      found = True
                      row = [date,True, profilename , profilename+"/"+img_path ];
                      image_details_list.append(row)
                   if precount == len(preds) and found == False:
                      #row = date + ',' + 'Many other faces' + ',' + img_path + '\n';
                      row = [date, False, 'Many other faces', profilename + "/" + img_path];
                      image_details_list.append(row)
               else:
                   if len(preds) == 1:
                       name = pred[0]
                       if(name == profilename):
                           #row = date + ',' + name + ',' + img_path + '\n';
                           row = [date, True, name, profilename + "/" + img_path];
                           image_details_list.append(row)
                       else:
                           #row = date + ',' + 'Others' + ',' + img_path + '\n';
                           row = [date, False, 'Others', profilename + "/" + img_path];
                           image_details_list.append(row)

    print(image_details_list)
    flag = write_image_details_db(image_details_list,instagram)
    return flag

def write_image_details_db(image_details_list,instagram):
    '''
    This function takes the list and write into the DB
    :param image_details_list:
    :param instagram:
    :return:
    '''

    for rec in image_details_list:
        date = rec[0]
        format_str = '%Y-%m-%d'  # The format
        datetime_obj = datetime.strptime(date, format_str)
        posted_on = datetime_obj.strftime('"%y/%m/%d"')
        selfie = rec[1]
        person = rec[2]
        image_path = rec[3]
        ##Inserting a post to database
        insql = "INSERT INTO application_picture (instagram,posted_on,selfie,person,image_path ) " \
                "VALUES ('%s','%s','%s','%s','%s')" \
                %(instagram, datetime_obj, selfie, person, image_path)
        print(insql)
        conn.execute(insql)
        conn.commit()
    return True


def predict(X_img_path, knn_clf = None, model_save_path ="", DIST_THRESH = .5):
    """
    recognizes faces in given image, based on a trained knn classifier

    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_save_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param DIST_THRESH: (optional) distance threshold in knn classification. the larger it is, the more chance of misclassifying an unknown person to a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'N/A' will be passed.
    """

    if not isfile(X_img_path) or splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        return ("Invalid", 'Not valid Image',X_img_path)
        #raise Exception("invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_save_path == "":
        raise Exception("must supply knn classifier either thourgh knn_clf or model_save_path")

    if knn_clf is None:
        with open(model_save_path, 'rb') as f:
            knn_clf = pickle.load(f)

    X_img = face_recognition.load_image_file(X_img_path)
    X_faces_loc = face_locations(X_img)
    if len(X_faces_loc) == 0:
        return [('No face detected' ,'', X_img_path)]

    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_faces_loc)

    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)

    is_recognized = [closest_distances[0][i][0] <= DIST_THRESH for i in range(len(X_faces_loc))]

    # predict classes and cull classifications that are not with high confidence
    # return [(pred, loc) if rec else ("N/A", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_faces_loc, is_recognized)]
    # returning file name
    return [(pred, loc,X_img_path) if rec else ("N/A", loc,X_img_path) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_faces_loc, is_recognized)]
###########Image Analysis

def startjob():

    cursor = conn.execute("SELECT * from application_users WHERE state = 'pending';")
    for row in cursor:
        profile = row[3]
        extract_information(profile)
        #print("ID = ", row)
    #extract_information(profile,profilepath)

if __name__ == '__main__':
    startjob()
