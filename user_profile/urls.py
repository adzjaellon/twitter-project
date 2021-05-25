from django.urls import path, include
from .views import ProfileDetail, FollowUser, RegisterUser
from django.contrib.auth import views as auth_views

app_name = 'profile'

urlpatterns = [
    path('<slug:slug>/profile/', ProfileDetail.as_view(), name='profile-details'),
    path('follow/', FollowUser.as_view(), name='follow'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
