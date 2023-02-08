from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('shorten', views.shorten, name="shorten"),
]