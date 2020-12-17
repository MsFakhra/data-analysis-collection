import sqlite3
from instaloader import Instaloader, Profile
from os import listdir
from os.path import isdir, join, isfile, splitext
import face_recognition
from face_recognition import face_locations
# from face_recognition.cli import image_files_in_folder
from face_recognition.face_detection_cli import image_files_in_folder
from math import sqrt
from sklearn import neighbors
import pickle
from datetime import datetime


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
    print("Training")
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
    print("Training complete")
    return knn_clf

instaLoader = Instaloader()
training_folder = 'project/application/static/media'
knn_clf = train(training_folder) #image knn classifier
conn = sqlite3.connect('project/db.sqlite3') #Database
#print("Opened database successfully")


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
            json = instaLoader.download_post(post,profilepath)
        posts.append(post)
        counter += 1
        print(counter)
    return posts

######################### Posts Extraction

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

        ##Inserting a post to database
        insql = "INSERT INTO application_posts (user_id,instagram,posted_on,post_url,hashtags,mentions,tagged_users,is_video,likes,caption ) " \
                "VALUES ('%d','%s','%s','%s','%s','%s','%s','%s','%d','%s')" \
                % (user_id,instagram,datetime_object,post_url,'Removed','Removed','Removed',is_video,likes,caption)
        print(insql)
        conn.execute(insql)
        conn.commit()
    #print('should update posts in db and then update processed as true')
    return processed;


def extract_information(id):
    print("Extracting Information")
    cursor = conn.execute("SELECT instagram from application_users WHERE id =" + str(id) + ";")
    for row in cursor:
        profilename = row[0]
    print(profilename)
    if('@' in profilename):
        profilename = profilename.replace('@','')
    profilepath = profilename  # Obtain profile
    profile = Profile.from_username(instaLoader.context, profilename)
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
            "private = " + str(private) + "," \
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

        #send_email(id)
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
        #send_email(id)

    print(profilename + "complete and id" + str(id))
    return private

def startjob():
    print("Job started")
    cursor = conn.execute("SELECT * from application_users WHERE state = 'pending' AND invalid = 0;")
    for row in cursor:
        id = row[0]
        print(id)
        extract_information(id)

if __name__ == '__main__':
    print("main")
    startjob()

