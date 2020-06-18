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
from face_recognition.cli import  image_files_in_folder
import re

#Tone Analysis
from watson_developer_cloud import ToneAnalyzerV3
apikey = 'wGySQLw3nxEOhEirYSvAZScum9v_1_VoA8lKZYMi6ip-'
urlref = 'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/618c6917-36fa-4dd7-a10b-8df2ed184446'
version = '2020-02-20'#'2020-02-21'

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



#######initializations
L = Instaloader()
#analyzer = initializeAnalyzer()


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


#one post usmanmaliktest
SINCE = datetime(2020, 5, 1)    #yyyy-mm-dd
UNTIL = datetime(2020,6,1)

def extract_information(profilename,path):
    #here create the basic model for user info; NPI is not here
    #path is image path
    profilepath = profilename    # Obtain profile
    profile = Profile.from_username(L.context, profilename)
    print("followers: ", profile.followers);
    print("full name: ", profile.full_name);
    print("biography: ", profile.biography);
    print("media count:", profile.mediacount);
    print("followees", profile.followees);
    posts = extract_posts(profile,profilepath)
    cmt = process_posts(posts,profilename)
    ########## TO-DO ###########
    # Here check if record is already in DB then no need to train for images then
    model_save_path = "./model/model.txt"
    knn_clf = train('TrainingDataset',model_save_path)
    process_Images(profilename,model_save_path)

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
            return cmtlist
    return [];
            #save this in comments

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
            process_conversations_emotions(convlist, tone_analyzer)
            return convlist

            '''processEmotion(msg)
            cmtlist.append(msg)
            prevscore = TextScore(msg.sentiment,msg.compscore)
            for rep in replyList:
                processEmotion(rep)
                if (rep.sentiment == "Neutral" or rep.sentiment == "Analytical"):
                    if (prevscore.tone == "Anger" or prevscore.tone == "Negative"):
                        score = prevscore;
                        rep.setEmotion(score)
                cmtlist.append(rep)'''
    return cmtlist;


def processEmotion(msg):
    text = msg.message
    #analyzing emotion of the text

    '''sentiment = processTexts(analyzer,text)
    msg.sentiment = sentiment.tone
    msg.compscore = sentiment.score
'''
def process_conversations_emotions(convlist,tone_analyzer):
    #INPUT: convlist contain messages with author details
    #OUTPT: convlist with emotions
    message = convlist[0]
    #making single conversation => saving API calls
    conv = message.message + ". <br>. "
    replies = convlist[1]
    for reply in replies:
        #print(reply.message)
        conv = conv + reply.message + ". <br>. "

    result = ta.processTexts(tone_analyzer,conv)

    ##############iteration of results
    # making one message
    removeitem = [{
        'text': "<br>.",
        'score': -1000,
        'tone_name': ''}]

    index = 0;
    length = len(result)
    sentences = []
    sentence = []
    while (index < length):
        item = result[index]
        if (item == removeitem):
            sentences.append(sentence)
            sentence = []
        else:
            value = item.pop(0)
            sentence.append(value)
        index += 1
    # Analytical	Anger	Fear	Joy	Sadness	Tentative	Confident	Positive	Negative	Neutral
    Emotions = ['Anger', 'Fear', 'Joy', 'Sadness', 'Disgust']
    Style = ['Analytical', 'Confident', 'Tentative']

    '''for msg in sentences:
        print(msg)
    '''

    ########### making conversation
    #extracting one emotion for a conversation
    conversation = []

    for msg in sentences:
        msgslist = msg
        message_result = {'text': '', 'tone_name': '', 'score': 0}
        message = msgslist[0];
        message_result['score'] = message.get('score')
        message_result['tone_name'] = message.get('tone_name')
        message_result['text'] = message.get('text')
        index = 1
        while index < len(msgslist):
            dic = msgslist[index];
            # message = {key: message.get(key,' ')+dic[key] for key in dic.keys()}
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
    comment.sentiment = sentiment
    comment.compscore = score

    i = 1;
    while i < len(convlist):
        tone_analysis = conversation[i]
        text,score,sentiment = extractTone(tone_analysis)
        reply = convlist[1][i - 1]
        reply.sentiment = sentiment
        reply.compscore = score
        i += 1


def Taggedcomment(text):
    hindex = -1;
    hindex = text.find('#')
    if(hindex > -1):
        return True;
    else:
        return False;


######################### Tone Analysis

def processTexts(tone_analyzer,text):
    # INPUT: process multiple texts seperated by .<br>.
    # OUTPUT: return dictionary containing score of all sentences with score. Sentences seperated by '.' or .<br>.
    result = []
    tone_analysis = tone_analyzer.tone({'text': text}, content_type='application/json').get_result()

    for key, value in tone_analysis.items():
        key_value = key
        if(key_value == 'sentences_tone'):
            sentences_list = value #dict
            for sentence in sentences_list:
                jsoncorrespondance = extractToneCorrespondence(sentence)
                result.append(jsoncorrespondance)
    return result

##########################Tone Analysis end

###########Image Analysis

def process_Images(profilename,model_save_path):
    trainingfolder = 'TrainingDataset'
    predictionfolder = profilename
    print("predicting")
    imageno = 1;
    for img_path in listdir(predictionfolder):
        preds = predict(join(predictionfolder, img_path) ,knn_clf=knn_clf,model_save_path = model_save_path)
        print("preds: ",preds)
        for pred in preds:
           row = ''
           location = pred[1]
           name = pred[0]
        #   yy, mm = extractdatetime(img_path);
           if(name != "N/A" and len(preds) > 1):
               row = True
             #row = yy + '-' + mm + ',' + name +',' + img_path + '\n';
           else:
             if len(preds) == 1:
                 #row = yy + '-' + mm + ',' + name + ',' + img_path + '\n';
                row = True
           print(row)
            #fd.write(row)
            # draw_preds(join("knn_examples/test", img_path), preds)return True


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
        raise Exception("invalid image path: {}".format(X_img_path))

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
