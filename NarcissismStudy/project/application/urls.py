from django.urls import path
from application import views

urlpatterns = [
    path('', views.index, name='index'),
    path('step2', views.step2, name='step2'),
    path('thankyou', views.thankyou, name='thankyou'),

    path('inputdata', views.inputdata, name='inputdata'),
]