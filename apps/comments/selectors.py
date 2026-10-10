from django.db.models import Prefetch

from .models import Comment


def get_comment_by_id(comment_id):
    return Comment.objects.filter(id=comment_id).first()


def post_comments_list(post_id, ordering='-created_at'):
    replies = Comment.objects.select_related('user').order_by('created_at')

    return (
        Comment.objects
        .filter(post_id=post_id, parent__isnull=True)
        .select_related('user')
        .prefetch_related(Prefetch('replies', queryset=replies))
        .order_by(ordering)
    )

