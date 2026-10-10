from django.urls import path
from .views import CreateCommentView, UpdateCommentView, DeleteCommentView

urlpatterns = [
    path('<int:post_id>/comments/', CreateCommentView.as_view(), name='create-comment'),
    path('comments/<int:comment_id>/', UpdateCommentView.as_view(), name='update-comment'),
    path('comments/<int:comment_id>/delete/', DeleteCommentView.as_view(), name='delete-comment'),
]
