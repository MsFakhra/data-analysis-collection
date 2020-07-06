from django.urls import path
from application import views

urlpatterns = [
    path('', views.index, name='index'),
    path('step2', views.step2, name='step2'),
    path('thankyou', views.thankyou, name='thankyou'),
<<<<<<< HEAD
    path('results',views.profile_results, name = "profile_results")
=======
    path('profile_results',views.profile_results, name = "profile_results")
>>>>>>> a0c7b29b83e6330cf254b8141db0fcab33ea20b3
]