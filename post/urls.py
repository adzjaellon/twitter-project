from django.urls import path, include
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetails.as_view(), name='post-details'),
    path('search/', views.search, name='search'),
    path('comment-delete/<pk>/', views.CommentDelete.as_view(), name='comment-delete'),
    path('comment-update/<pk>/', views.CommentUpdate.as_view(), name='comment-update')
]
