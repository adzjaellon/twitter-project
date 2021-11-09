from django.urls import path, reverse_lazy
from .views import ProfileDetail, FollowUser, RegisterUser, ProfileUpdate, ContactForm, ProfileSearch, UserUpdate
from django.contrib.auth import views as auth_views

app_name = 'profile'

urlpatterns = [
    path('<slug:slug>/details/', ProfileDetail.as_view(), name='profile-details'),
    path('<slug:slug>/update/', ProfileUpdate.as_view(), name='profile-update'),
    path('<int:pk>/update-user/', UserUpdate.as_view(), name='user-update'),
    path('search_profile/', ProfileSearch.as_view(), name='profile-search'),
    path('support/', ContactForm.as_view(), name='contact'),
    path('follow/', FollowUser.as_view(), name='follow'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user_profile/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('profile:password_change_done'), template_name='password/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password/password_change_done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user_profile/registration/password_reset_form.html', email_template_name='user_profile/registration/password_reset_email.html', success_url=reverse_lazy('profile:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user_profile/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user_profile/registration/password_reset_confirm.html', success_url=reverse_lazy('profile:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
