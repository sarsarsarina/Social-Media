from django.db import transaction
from .models import Post, PostMedia


def create_post(owner, validated_data):
    caption = validated_data.get('caption', '')
    visibility = validated_data.get('visibility', Post.Visibility.PUBLIC)
    comments_enabled = validated_data.get('comments_enabled', True)
    images = validated_data.get('images', [])
    videos = validated_data.get('videos', [])
    
    with transaction.atomic():
        post = Post.objects.create(
            owner=owner,
            caption=caption,
            visibility=visibility,
            comments_enabled=comments_enabled
        )

        media_objects = []
        order = 0

        for image in images:
            media_objects.append(PostMedia(
                post=post,
                file=image,
                media_type=PostMedia.MediaType.IMAGE,
                order=order
            ))
            order += 1

        for video in videos:
            media_objects.append(PostMedia(
                post=post,
                file=video,
                media_type=PostMedia.MediaType.VIDEO,
                order=order
            ))
            order += 1

        if media_objects:
            PostMedia.objects.bulk_create(media_objects)

    return post
