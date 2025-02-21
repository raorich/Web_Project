from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Routes that can we access in our websites

urlpatterns = [
    path('', views.home, name='home')
] 