from django.urls import path
from . import views


urlpatterns = [
    path('like/post/<int:post_id>/', views.LikePostView.as_view(), name='like_post'),
    path('unlike/post/<int:post_id>/', views.UnlikePostView.as_view(), name='unlike_post'),
    path('post/likes/list/<int:post_id>/', views.PostLikesListView.as_view(), name='postlikes_list'),
]
