import pathlib
import os
from django.http import HttpResponse
from django.shortcuts import render

def hello_world(request):
    return HttpResponse("request, 'hello_world.html', {}")

def inputdata(request):
    # This just create the folder where I want to save the image.
    profile = 'usmanmaliktest'
    path = '/TrainingDataset/' + profile
    if not os.path.exists(path):
        path = pathlib.Path('TrainingDataset/' , profile)
        path.parent.mkdir(parents=True, exist_ok=True)
    return HttpResponse("Processed")

