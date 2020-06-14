import pathlib
import os
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from application.models import Users

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
    # This just create the folder where I want to save the image.
    profile = 'usmanmaliktest'
    path = '/TrainingDataset/' + profile
    if not os.path.exists(path):
        path = pathlib.Path('TrainingDataset/' , profile)
        path.parent.mkdir(parents=True, exist_ok=True)
    return HttpResponse("Processed")

