from django.urls import path
from . import views

urlpatterns = [
        path('me/', views.MyPostsView.as_view(), name='my_posts'),
]