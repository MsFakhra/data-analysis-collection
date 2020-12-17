import sqlite3
from instaloader import Instaloader, Profile

conn = sqlite3.connect('project/db.sqlite3')
instaLoader = Instaloader()


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

def startjob():
    print("Job started")
    cursor = conn.execute("SELECT * from application_users WHERE state = 'pending' AND invalid = 0;")
    for row in cursor:
        id = row[0]
        extract_information(id)

if __name__ == '__main__':
    print("main")
    startjob()

