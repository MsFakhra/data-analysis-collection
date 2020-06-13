import pathlib
import os
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def step2(request):
    return render(request, 'step2.html', {})

def thankyou(request):
    return render(request, 'thankyou.html', {})

def inputdata(request):
    # This just create the folder where I want to save the image.
    profile = 'usmanmaliktest'
    path = '/TrainingDataset/' + profile
    if not os.path.exists(path):
        path = pathlib.Path('TrainingDataset/' , profile)
        path.parent.mkdir(parents=True, exist_ok=True)
    return HttpResponse("Processed")

