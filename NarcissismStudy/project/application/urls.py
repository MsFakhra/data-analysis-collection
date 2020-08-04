from django.urls import path
from application import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('/whatwedo', views.whatwedo, name='whatwedo'),
    #path('/contactus', views.contactus, name='contactus'),

    path('step2', views.step2, name='step2'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('results',views.profile_results, name = "profile_results")

]