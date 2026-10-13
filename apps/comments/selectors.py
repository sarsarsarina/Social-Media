from django.db.models import Count

from .models import Comment


def get_comment_by_id(comment_id):
    return Comment.objects.filter(id=comment_id).first()


def post_comments_list(post_id, ordering='-created_at'):
    return (
        Comment.objects
        .filter(post_id=post_id, parent__isnull=True)
        .select_related('user')
        .annotate(replies_count=Count('replies'))
        .order_by(ordering)
    )

