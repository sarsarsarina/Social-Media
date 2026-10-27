from django.urls import path
from . import views


urlpatterns = [
    path('like/post/<int:post_id>/', views.LikePost.as_view(), name='like_post'),
    path('unlike/post/<int:post_id>/', views.UnlikePost.as_view(), name='unlike_post')
]
