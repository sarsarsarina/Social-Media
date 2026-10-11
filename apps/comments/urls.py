from django.urls import path

from .views import (
    CreateCommentView,
    DeleteCommentView,
    PostCommentsView,
    UpdateCommentView,
)

urlpatterns = [
    path('<int:post_id>/comments/', CreateCommentView.as_view(), name='create-comment'),
    path('comments/<int:comment_id>/', UpdateCommentView.as_view(), name='update-comment'),
    path('comments/<int:comment_id>/delete/', DeleteCommentView.as_view(), name='delete-comment'),
    path('<int:post_id>/comments/list/', PostCommentsView.as_view(), name='post-comments'),
]
