from instaloader import Instaloader, Profile
from datetime import datetime
import itertools
from itertools import dropwhile, takewhile
from django.contrib.auth.models import User
import time

#Tone Analysis
from watson_developer_cloud import ToneAnalyzerV3
apikey = 'wGySQLw3nxEOhEirYSvAZScum9v_1_VoA8lKZYMi6ip-'
urlref = 'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/618c6917-36fa-4dd7-a10b-8df2ed184446'
version = '2020-02-20'#'2020-02-21'

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

#######initializations
L = Instaloader()
#analyzer = initializeAnalyzer()

#######initializations

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


#one post usmanmaliktest
SINCE = datetime(2020, 5, 1)    #yyyy-mm-dd
UNTIL = datetime(2020,6,1)

def extract_information(profilename,path):
    #here create the basic model for user info; NPI is not here
    #path is image path
    profilepath = profilename

    # Obtain profile
    profile = Profile.from_username(L.context, profilename)
    print("followers: ", profile.followers);
    print("full name: ", profile.full_name);
    print("biography: ", profile.biography);
    print("media count:", profile.mediacount);
    print("followees", profile.followees);
    posts = extract_posts(profile,profilepath)
    process_posts(posts,profilename)

def extract_posts(profile,profilepath):
    # Obtain posts sorted w.r.t date
    posts = []
    posts_sorted_by_date = sorted(profile.get_posts(), key=lambda p: p.date, reverse=False)
    for post in takewhile(lambda p: p.date <= UNTIL, dropwhile(lambda p: p.date <  SINCE, posts_sorted_by_date)):
    #for post in posts_sorted_by_date:
        print (post.caption)
        json = L.download_post(post,profilepath)
        posts.append(post)
    #print(len(posts_sorted_by_date))
    return posts


def process_posts(posts,profilename):
    for post in posts:
        print('caption', post.caption)
        if(post.comments > 0):
            cmtlist = process_comments(post,profilename)
            #save this in comments

def process_comments(post,profilename):
    cmtlist = [];
    comments = post.get_comments()
    ###processing comments
    for cmt in comments:
        comment = cmt.text.replace('\n', ' ').replace('\r', '');
        stamp = cmt.created_at_utc;
        msg = Message(True, comment, cmt.owner.username,stamp);
        ############# analyzing comment for like ... a narcisst will prefer to like his praise
        answer = cmt.answers
        ####Observing likes
        like_count = 0;
        import inspect2
        dict = inspect2.getgeneratorlocals(answer)
        items = dict.items();
        for p_id, p_info in items:
            #print("\nNode ID:", p_id)
            if(p_id == 'node'):
                for key in p_info:
                    #print(key + ':', p_info[key])
                    if(key =='edge_liked_by'):
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
                if(name == profilename):
                    influencerinvolved = True
                reply = reply.replace('\n', ' ').replace('\r', '');
                stamp = r.created_at_utc#.created_at_utc.isoformat();
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
            processEmotion(msg)
            cmtlist.append(msg)
            prevscore = TextScore(msg.sentiment,msg.compscore)
            for rep in replyList:
                processEmotion(rep)
                if (rep.sentiment == "Neutral" or rep.sentiment == "Analytical"):
                    if (prevscore.tone == "Anger" or prevscore.tone == "Negative"):
                        score = prevscore;
                        rep.setEmotion(score)
                cmtlist.append(rep)
    return cmtlist;

def processEmotion(msg):
    text = msg.message
    #analyzing emotion of the text
    '''sentiment = processText(analyzer,text)
    msg.sentiment = sentiment.tone
    msg.compscore = sentiment.score
'''
def Taggedcomment(text):
    hindex = -1;
    hindex = text.find('#')
    if(hindex > -1):
        return True;
    else:
        return False;


######################### Tone Analysis
class ToneScore(object):
    def __init__(self, tone,score):
        self.tone = tone
        self.score = score


def processText(tone_analyzer,text):

    # takes 'ToneInput' key values in input text
    input_texts = text

    # sends data and requests the analysis
    tone_analysis = tone_analyzer.tone({'text': input_texts}, 'application/json').get_result()
    for key, value in tone_analysis.items():
        key_value = key
        if(key_value == 'document_tone'):
            values_list = value #dict
            poped_list = values_list.pop('tones')
            max = -1;
            HighScore = ToneScore('null',max)
            for item in poped_list:
                tone_name = item.pop('tone_name')
                score = item.pop('score')
                if(max == -1):
                    HighScore = ToneScore(tone_name, score)
                    max = score
                if(score > max):
                    max = score
                    HighScore = ToneScore(tone_name,max)
            return HighScore

##########################Tone Analysis end

###########Image Analysis

###########Image Analysis