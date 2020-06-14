import os
import pathlib
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from application.models import Users
from .tasks import extract_information

def index(request):
    return render(request, 'index.html', {})

def step2(request):
    user = Users(
        full_name = request.POST['full_name'],
        email = request.POST['email'],
        instagram = request.POST['instagram'],
        created_at = datetime.datetime.now(),
    )
    user.save()
    print (request.FILES)
    return render(request, 'step2.html', {})

def thankyou(request):
    return render(request, 'thankyou.html', {})

def inputdata(request):
    # This will create the folder where i want to save the image
    profile = 'usmanmaliktest'
    #profile = 'usmanahmedmalik'
    profilepath = 'TrainingDataset/' + profile

    if not os.path.exists(profilepath):
        path = pathlib.Path('TrainingDataset/' + profile)
        path.mkdir(exist_ok=True,parents=True)
    extract_information(profile,profilepath)
    return HttpResponse("Hello I am Processed")

