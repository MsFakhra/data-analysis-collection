import os
import pathlib
from django.http import HttpResponse
from django.shortcuts import render
from .tasks import extract_information
from .tasks import process_Images

def index(request):
    return render(request, 'index.html', {})

def step2(request):
    return render(request, 'step2.html', {})

def thankyou(request):
    return render(request, 'thankyou.html', {})

def inputdata(request):
    # This will create the folder where i want to save the image
    profile = 'usmanmaliktest'
    profile = 'annam.ahmad'
    #profile = 'usmanahmedmalik'
    profilepath = 'TrainingDataset/' + profile

    if not os.path.exists(profilepath):
        path = pathlib.Path('TrainingDataset/' + profile)
        path.mkdir(exist_ok=True,parents=True)
    extract_information(profile,profilepath)   
    return HttpResponse("Hello I am Processed")

