from django.urls import path
from application import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
]