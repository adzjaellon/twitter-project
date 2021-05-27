from django.urls import path, reverse_lazy
from .views import ProfileDetail, FollowUser, RegisterUser, ProfileUpdate
from django.contrib.auth import views as auth_views

app_name = 'profile'

urlpatterns = [
    path('<slug:slug>/profile/', ProfileDetail.as_view(), name='profile-details'),
    path('<slug:slug>/profile/update/', ProfileUpdate.as_view(), name='profile-update'),
    path('follow/', FollowUser.as_view(), name='follow'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('profile:password_change_done'), template_name='password/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password/password_change_done.html'), name='password_change_done'),
]
