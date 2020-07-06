import json
import os
import pathlib
import datetime

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from application.models import Users,Posts,Picture
from .tasks import extract_information
from .tasks import process_Images

import sqlite3

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
    questionList = [
        ['I have a natural talent for influencing people.', 'I am not good at influencing people.'],
        ['Modesty doesn\'t become me.', 'I am essentially a modest person.'],
        ['I would do almost anything on a dare.', 'I tend to be a fairly cautious person.'],
        ['When people compliment me I sometimes get embarrassed.', 'I know that I am good because everybody keeps telling me so.'],
        ['The thought of ruling the world frightens the hell out of me.', 'If I ruled the world it would be a better place.'],
        ['I can usually talk my way out of anything.', 'I try to accept the consequences of my behavior.'],
        ['I prefer to blend in with the crowd.', 'I like to be the center of attention.'],
        ['I will be a success.', 'I am not too concerned about success.'],
        ['I am no better or worse than most people.', 'I think I am a special person.'],
        ['I am not sure if I would make a good leader.', 'I see myself as a good leader.'],
        ['I am assertive.', 'I wish I were more assertive.'],
        ['I like to have authority over other people.', 'I don\'t mind following orders.'],
        ['I find it easy to manipulate people.', 'I don\'t like it when I find myself manipulating people.'],
        ['I insist upon getting the respect that is due me.', 'I usually get the respect that I deserve.'],
        ['I don\'t particularly like to show off my body.', 'I like to show off my body.'],
        [' I can read people like a book.', 'People are sometimes hard to understand.'],
        ['If I feel competent I am willing to take responsibility for making decisions.', 'I like to take responsibility for making decisions.'],
        ['I just want to be reasonably happy.', 'I want to amount to something in the eyes of the world.'],
        ['My body is nothing special.', 'I like to look at my body.'],
        ['I try not to be a show off.', 'I will usually show off if I get the chance.'],
        ['I always know what I am doing.', 'Sometimes I am not sure of what I am doing.'],
        ['I sometimes depend on people to get things done.', 'I rarely depend on anyone else to get things done.'],
        ['Sometimes I tell good stories.', 'Everybody likes to hear my stories.'],
        ['I expect a great deal from other people.', 'I like to do things for other people.'],
        ['I will never be satisfied until I get all that I deserve.', 'I take my satisfactions as they come.'],
        ['Compliments embarrass me.', 'I like to be complimented.'],
        ['I have a strong will to power.', 'Power for its own sake doesn\'t interest me.'],
        ['I don\'t care about new fads and fashions.', 'I like to start new fads and fashions.'],
        ['I like to look at myself in the mirror.', 'I am not particularly interested in looking at myself in the mirror.'],
        ['I really like to be the center of attention.', 'It makes me uncomfortable to be the center of attention.'],
        ['I can live my life in any way I want to.', 'People can\'t always live their lives in terms of what they want.'],
        ['Being an authority doesn\'t mean that much to me.', 'People always seem to recognize my authority.'],
        ['I would prefer to be a leader.', 'It makes little difference to me whether I am a leader or not.'],
        ['I am going to be a great person.', 'I hope I am going to be successful.'],
        ['People sometimes believe what I tell them.', 'I can make anybody believe anything I want them to.'],
        ['I am a born leader.', 'Leadership is a quality that takes a long time to develop.'],
        ['I wish somebody would someday write my biography.', 'I don\'t like people to pry into my life for any reason.'],
        ['I get upset when people don\'t notice how I look when I go out in public.', 'I don\'t mind blending into the crowd when I go out in public.'],
        ['I am more capable than other people.', 'There is a lot that I can learn from other people.'],
        ['I am much like everybody else.', 'I am an extraordinary person.'],
    ]
    return render(request, 'step2.html', {'questionList':  questionList})

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
<<<<<<< HEAD
    user = Users.objects.get(instagram='annam.ahmad')
=======
    pics = Picture.objects.all()
    for p in pics:
        print(p.posted_on)
    return HttpResponse("done")


    #AIM: database extraction of objects
    user = Users.objects.get(instagram = 'annam.ahmad')
>>>>>>> a0c7b29b83e6330cf254b8141db0fcab33ea20b3

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
<<<<<<< HEAD
    #obj = Posts.objects.filter(user_id= id)#1792)  # https://www.youtube.com/watch?v=vCX6Tpb9sP8
    obj = Posts.objects.filter(id= 1792)
    '''context = {
        "instagram": obj.instagram,
        "caption": obj.caption,
        "posted_on": obj.posted_on,
        "post_url": obj.post_url,
        "hashtags": obj.hashtags
    }'''
    context = {"object":obj}

    return render(request, "profile_results.html", context)
=======
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

def test(request):
    allUsers = Users.objects.all()
    for user in allUsers:
        print(user.created_at)

    return render(request, 'test.html', {'users': allUsers})

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
>>>>>>> a0c7b29b83e6330cf254b8141db0fcab33ea20b3
