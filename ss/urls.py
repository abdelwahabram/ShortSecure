from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('shorten', views.shorten, name="shorten"),
    path('accounts/register', views.register, name="register"),
    path('<str:short>', views.redirectUrl, name="redirect")
]
