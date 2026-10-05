from django.urls import path
from . import views

urlpatterns = [
        path('me/', views.MyPostsView.as_view(), name='my_posts'),
        path('create/', views.CreatePostView.as_view(), name='create_post'),
        path('<int:post_id>/', views.UpdatePostView.as_view(), name='update_post'),
]