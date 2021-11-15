from django.urls import path, include
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetails.as_view(), name='post-details'),
    path('post/<slug:slug>/update/', views.PostUpdate.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', views.PostDelete.as_view(), name='post-delete'),
    path('search/', views.Search.as_view(), name='search'),
    path('comment-delete/<int:pk>/', views.CommentDelete.as_view(), name='comment-delete'),
    path('comment-update/<int:pk>/', views.CommentUpdate.as_view(), name='comment-update'),
    path('tag/<str:name>/', views.PostTagList.as_view(), name='tag-posts'),
    path('create/', views.PostCreate.as_view(), name='create-post'),
    path('like/', views.LikePost.as_view(), name='like-post')
]
