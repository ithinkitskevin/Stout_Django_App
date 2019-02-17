from django.views import generic
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url('', views.BeerView, name='beerView'),
]