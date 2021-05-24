from django.urls import path, include
from .views import ProfileDetail, FollowUser

app_name = 'profile'

urlpatterns = [
    path('<slug:slug>/profile/', ProfileDetail.as_view(), name='profile-details'),
    path('follow/', FollowUser.as_view(), name='follow')

]
