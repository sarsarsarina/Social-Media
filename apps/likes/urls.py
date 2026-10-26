from django.urls import path
from . import views


urlpatterns = [
    path('like/post/<int:post_id>/', views.LikePost.as_view(), name='like_post')
]
