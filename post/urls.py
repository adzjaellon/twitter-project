from django.urls import path, include
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>', views.PostDetails.as_view(), name='post-details')
]
