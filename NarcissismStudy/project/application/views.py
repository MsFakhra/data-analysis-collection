import os
import pathlib
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from application.models import Users
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