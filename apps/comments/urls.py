from django.urls import path
from .views import CreateCommentView, UpdateCommentView

urlpatterns = [
    path('<int:post_id>/comments/', CreateCommentView.as_view(), name='create-comment'),
    path('comments/<int:comment_id>/', UpdateCommentView.as_view(), name='update-comment'),
]
