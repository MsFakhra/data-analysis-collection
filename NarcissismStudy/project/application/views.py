import os

from django.http import HttpResponse
from django.shortcuts import render

def hello_world(request):
    return HttpResponse("request, 'hello_world.html', {}")

def inputdata(request):
    # This just create the folder where I want to save the image.
    profile = 'usmanmaliktest'
    if not os.path.exists('/TrainingDataset/' + profile):
        os.mkdir('/TrainingDataset/' + profile)
    return HttpResponse("Processed")

