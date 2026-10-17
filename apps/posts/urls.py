from django.urls import path
from . import views

urlpatterns = [
        path('me/', views.MyPostsView.as_view(), name='my_posts'),
        path('create/', views.CreatePostView.as_view(), name='create_post'),
        path('<int:post_id>/', views.UpdatePostView.as_view(), name='update_post'),
        path('<int:post_id>/delete/', views.DeletePostView.as_view(), name='delete_post'),
        path('<int:post_id>/detail/', views.PostDetailView.as_view(), name='post_detail'),
        path('', views.PostListView.as_view(), name='post_list'),
        path('explore/', views.ExploreView.as_view(), name='explore'),
        path('saved/post/<int:post_id>/', views.SavedPostView.as_view(), name='saved_post'),
        path('unsaved/post/<int:post_id>/', views.UnsavePostView.as_view(), name='unsaved_post'),
]