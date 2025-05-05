from django.urls import path
from . import views

# Routes that can we access in our websites

urlpatterns = [
    path('', views.home, name='home'),
    # ----------- Login --------------#
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('producto/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search-products/', views.search_products, name='search_products'),

] 