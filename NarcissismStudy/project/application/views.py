import json
import os
import pathlib
import datetime

from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.http import HttpResponse
from django.shortcuts import render
from application.models import Users,Posts,Picture,Comment
from .tasks import extract_information
from .tasks import process_Images
from django.db.models import Avg, Max

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
    request.session['user'] = user.id

    handle_uploaded_file(request.FILES['selfie'],instagram)
    questionList = [
        ['I have a natural talent for influencing people.', 'I am not good at influencing people.', '1', '0'],
        ['Modesty doesn\'t become me.', 'I am essentially a modest person.', '1', '0'],
        ['I would do almost anything on a dare.', 'I tend to be a fairly cautious person.', '1', '0'],
        ['When people compliment me I sometimes get embarrassed.', 'I know that I am good because everybody keeps telling me so.', '0', '1'],
        ['The thought of ruling the world frightens the hell out of me.', 'If I ruled the world it would be a better place.', '0', '1'],
        ['I can usually talk my way out of anything.', 'I try to accept the consequences of my behavior.', '1', '0'],
        ['I prefer to blend in with the crowd.', 'I like to be the center of attention.', '0', '1'],
        ['I will be a success.', 'I am not too concerned about success.', '1', '0'],
        ['I am no better or worse than most people.', 'I think I am a special person.', '0', '1'],
        ['I am not sure if I would make a good leader.', 'I see myself as a good leader.', '0', '1'],
        ['I am assertive.', 'I wish I were more assertive.', '1', '0'],
        ['I like to have authority over other people.', 'I don\'t mind following orders.', '1', '0'],
        ['I find it easy to manipulate people.', 'I don\'t like it when I find myself manipulating people.', '1', '0'],
        ['I insist upon getting the respect that is due me.', 'I usually get the respect that I deserve.', '1', '0'],
        ['I don\'t particularly like to show off my body.', 'I like to show off my body.', '0', '1'],
        [' I can read people like a book.', 'People are sometimes hard to understand.', '1', '0'],
        ['If I feel competent I am willing to take responsibility for making decisions.', 'I like to take responsibility for making decisions.', '0', '1'],
        ['I just want to be reasonably happy.', 'I want to amount to something in the eyes of the world.', '0', '1'],
        ['My body is nothing special.', 'I like to look at my body.', '0', '1'],
        ['I try not to be a show off.', 'I will usually show off if I get the chance.', '0', '1'],
        ['I always know what I am doing.', 'Sometimes I am not sure of what I am doing.', '1', '0'],
        ['I sometimes depend on people to get things done.', 'I rarely depend on anyone else to get things done.', '0', '1'],
        ['Sometimes I tell good stories.', 'Everybody likes to hear my stories.', '0', '1'],
        ['I expect a great deal from other people.', 'I like to do things for other people.', '1', '0'],
        ['I will never be satisfied until I get all that I deserve.', 'I take my satisfactions as they come.', '1', '0'],
        ['Compliments embarrass me.', 'I like to be complimented.', '0', '1'],
        ['I have a strong will to power.', 'Power for its own sake doesn\'t interest me.', '1', '0'],
        ['I don\'t care about new fads and fashions.', 'I like to start new fads and fashions.', '0', '1'],
        ['I like to look at myself in the mirror.', 'I am not particularly interested in looking at myself in the mirror.', '1', '0'],
        ['I really like to be the center of attention.', 'It makes me uncomfortable to be the center of attention.', '1', '0'],
        ['I can live my life in any way I want to.', 'People can\'t always live their lives in terms of what they want.', '1', '0'],
        ['Being an authority doesn\'t mean that much to me.', 'People always seem to recognize my authority.', '0', '1'],
        ['I would prefer to be a leader.', 'It makes little difference to me whether I am a leader or not.', '1', '0'],
        ['I am going to be a great person.', 'I hope I am going to be successful.', '1', '0'],
        ['People sometimes believe what I tell them.', 'I can make anybody believe anything I want them to.', '0', '1'],
        ['I am a born leader.', 'Leadership is a quality that takes a long time to develop.', '1', '0'],
        ['I wish somebody would someday write my biography.', 'I don\'t like people to pry into my life for any reason.', '1', '0'],
        ['I get upset when people don\'t notice how I look when I go out in public.', 'I don\'t mind blending into the crowd when I go out in public.', '1', '0'],
        ['I am more capable than other people.', 'There is a lot that I can learn from other people.', '1', '0'],
        ['I am much like everybody else.', 'I am an extraordinary person.', '0', '1'],
    ]

    return render(request, 'step2.html', {'questionList':  questionList})

def thankyou(request):
    i=1;
    score=0
    while i < 41:
        if 'question_' + str(i) in request.POST:
            score += int(request.POST['question_' + str(i)])
        i+=1

    user = Users.objects.get(id=request.session['user'])
    user.npi_score = score
    user.save()
    return render(request, 'thankyou.html', {'score': score})

def handle_uploaded_file(f,instagram):
    # os.mkdir('TrainingDataset/' + instagram)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media = os.path.join(BASE_DIR, 'application/static/media')

    profilepath = media + '/' + instagram

    if not os.path.exists(profilepath):
        path = pathlib.Path(profilepath)
        path.mkdir(exist_ok=True,parents=True)

    with open(profilepath + '/name.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

###### Projecting the data from the database

def profile_results(request):
    instagram = 'lisa_nolan'
    user = Users.objects.get(instagram = instagram)

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

    posts = Posts.objects.annotate(month=TruncMonth('posted_on')).values('month').annotate(total=Count('user_id')).filter(user_id= id)
    likes = Posts.objects.annotate(month=TruncMonth('posted_on')).values('month').annotate(avg_likes=Avg('likes')).filter(user_id= id)
    pictures = Picture.objects.annotate(month=TruncMonth('posted_on')).values('month','person').annotate(total=Count('instagram')).filter(instagram = id)
    comments = Comment.objects.annotate(month=TruncMonth('posted_on')).values('month', 'sentiment').annotate(
        total=Count('owner')).filter(owner = instagram)
    for row in comments:
        print(row)
    json_context = {
        "user":user,
        "posts":posts,
        "likes":likes,
        "pictures": pictures,
        "comments":comments
    }

    return render(request, "profile_results.html", json_context)# {'data': json_context})

def get_non_selfie_score(nselfie,val):
    for dic in nselfie:
        value = dic['month']
        if(value == val):
            return dic['total']
    return 0


def test(request):
    allUsers = Users.objects.all()
    for user in allUsers:
        print(user.created_at)

    return render(request, 'test.html', {'users': allUsers})