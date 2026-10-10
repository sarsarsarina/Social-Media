from .models import Comment

def get_comment_by_id(comment_id):
    return Comment.objects.filter(id=comment_id).first()