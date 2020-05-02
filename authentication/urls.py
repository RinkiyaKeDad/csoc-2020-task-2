from django.urls import path
from authentication.views import *

urlpatterns = [
    path('login/',loginView, name='loginView'),
    path('logout/',logoutView, name='logoutView'),
    path('register/',registerView, name='registerView'),
]