import os
import pathlib
from django.http import HttpResponse
from django.shortcuts import render
from .tasks import extract_information

def hello_world(request):
    return HttpResponse("request, 'hello_world.html', {}")

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

