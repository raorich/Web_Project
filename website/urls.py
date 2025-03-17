from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Routes that can we access in our websites

urlpatterns = [
    path('', views.home, name='home'),
    # ----------- Login --------------#
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
] 