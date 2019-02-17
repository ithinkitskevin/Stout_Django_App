from django.views import generic
from django.conf.urls import include, url
from . import views

urlpatterns = [
    
    url('home/$', views.HomeView, name='homeView'),
    url('', views.DrinkerView, name='drinkerView'),
]