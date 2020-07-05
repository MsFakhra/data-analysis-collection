import json
import os
import pathlib
import datetime

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from application.models import Users,Posts
from .tasks import extract_information
from .tasks import process_Images

def index(request):
    return render(request, 'index.html', {})

def step2(request):
    instagram = request.POST['instagram']
    user = Users(
        full_name = request.POST['full_name'],
        email = request.POST['email'],
        instagram = request.POST['instagram'],
        created_at = datetime.datetime.now(),
    )
    user.save()

    handle_uploaded_file(request.FILES['selfie'],instagram)
    return render(request, 'step2.html', {})

def thankyou(request):
    return render(request, 'thankyou.html', {})

def handle_uploaded_file(f,instagram):
    # os.mkdir('TrainingDataset/' + instagram)

    profilepath = 'TrainingDataset/' + instagram

    if not os.path.exists(profilepath):
        path = pathlib.Path('TrainingDataset/' + instagram)
        path.mkdir(exist_ok=True,parents=True)

    with open('TrainingDataset/' + instagram + '/name.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

###### Projecting the data from the database

def profile_results(request):
    #AIM: database extraction of objects
    user = Users.objects.get(instagram = 'annam.ahmad')

    id = user.id
    full_name = user.full_name
    email = user.email
    npi_score = user.npi_score
    biography = user.biography
    media_count = user.media_count
    followers = user.followers
    following = user.following

    profile = {  # getting data from queryset
        "full_name": full_name,
        "email": email,
        "npi_score": npi_score,
        "biography": biography,
        "media_count": media_count,
        "followers": followers,
        "following": following
    }
    obj = Posts.objects.filter(id=2401)  #https://www.youtube.com/watch?v=vCX6Tpb9sP8

    context = {
        "instagram" : obj.instagram,
        "caption"   : obj.caption,
        "posted_on" : obj.posted_on,
        "post_url" : obj.post_url,
        "hashtags" : obj.hashtags
    }

    return render(request,"profile_results.html",context)
    #queryset = Posts.objects.filter(user_id = id)
    #return HttpResponse(json.dumps(profile))


    '''
    queryset = Posts.objects.all().values('posted_on').annotate(count=Count('posted_on')).filter(user_id=id)
    rec = []
    for entry in queryset:
        rec.append(entry['posted_on'])
        
        
        
    
    queryset = Posts.objects.values('posted_on').annotate(count=Count(Posts.objects)).filter(user_id=id)

    posts = []
    for entry in queryset:
        post = {
            "instagram" : entry.instagram,
            "posted_on" : entry.posted_on,
            "post_url" : entry.post_url,
            "hashtags" : entry.hashtags,
            "mentions" : entry.mentions,
            "tagged_users" : entry.tagged_users,
            "is_video" : entry.is_video,
            "likes" : entry.likes,
            "caption" : entry.caption
        }
        posts.append(post)
    '''

    #return HttpResponse(json.dumps(profile))
    #return HttpResponse({'Data': json.dumps(posts)})

'''
data = []
    queryset = Posted.objects.all()
    for entry in queryset:
        name = entry.profilename.profilename
        if(name == "test"): #this is the object / record in the database
            profile = {     #getting data from queryset
                "name"  : name,
                "date"  : entry.date,
                "anger" : entry.anger,
                "fear"  :entry.fear,
                "joy"   :entry.joy,
                "sadness":entry.sadness,
                "disgust": entry.disgust,
                "neutral": entry.neutral,
                "positive": entry.positive,
                "negative": entry.negaitive
            }
            data.append(profile)

    context = {'Data': json.dumps(data)}
    return render(request,"basicinfo.html",context = context)'''