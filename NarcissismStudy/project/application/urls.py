from django.urls import path
from application import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('home', views.home, name='home'),
    path('whatwedo', views.whatwedo, name='whatwedo'),
    path('contactus', views.contactus, name='contactus'),
    path('register', views.register, name='register'),

    path('step2', views.step2, name='step2'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('results',views.profile_results, name = "profile_results")

]