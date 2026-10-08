from django.urls import path
from .views import CreateCommentView

urlpatterns = [
    path('<int:post_id>/comments/', CreateCommentView.as_view(), name='create-comment')
]
