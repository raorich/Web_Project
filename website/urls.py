from django.urls import path
from . import views


# Routes that can we access in our websites

urlpatterns = [
    path('', views.home, name='home'),
    # ----------- Login --------------#
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # ----------- Products --------------#
    path('producto/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search-products/', views.search_products, name='search_products'),
    # ----------- Profile --------------#
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('profile-bids/', views.profile_bids, name='profile_bids'),
    path('profile-stores/', views.profile_stores, name='profile_stores'),
    path('profile-history-acquision/', views.profile_history_acquision, name='profile_history_acquision'),
    path('add-user-store/', views.profile_add_user_store, name='profile_add_user_store'),
    path('add-new-store/', views.profile_create_store, name='profile_create_store'),
    path('remove-store/', views.profile_remove_store, name='profile_remove_store'),
    path('remove-user-store/', views.profile_remove_user_store, name='profile_remove_user_store'),
    path('edit-name-store/', views.profile_edit_name_store, name='profile_edit_name_store'),
] 