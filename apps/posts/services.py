from django.db import transaction
from .models import Post, PostMedia, SavedPost
from .selectors import get_post_by_id, post_list, is_post_saved
from rest_framework.exceptions import NotFound, ValidationError


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


def update_post(user, post_id, validated_data):
    post = get_post_by_id(post_id)

    if not post or post.owner != user:
        raise NotFound("Post not found")

    with transaction.atomic():
        if 'caption' in validated_data:
            post.caption = validated_data['caption']

        if 'visibility' in validated_data:
            post.visibility = validated_data['visibility']

        if 'comments_enabled' in validated_data:
            post.comments_enabled = validated_data['comments_enabled']

        post.save()

        new_images = validated_data.get('new_images', [])
        new_videos = validated_data.get('new_videos', [])
        remove_media_ids = validated_data.get('remove_media_ids', [])

        if remove_media_ids:
            PostMedia.objects.filter(id__in=remove_media_ids,post=post).delete()

        last_media = post.media.order_by('-order').first()
        order = last_media.order + 1 if last_media else 0

        media_objects = []

        for image in new_images:
            media_objects.append(PostMedia(
                post=post,
                file=image,
                media_type=PostMedia.MediaType.IMAGE,
                order=order
            ))
            order += 1

        for video in new_videos:
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


def delete_post(user, post_id):
    post = get_post_by_id(post_id)

    if not post or post.owner != user:
        raise NotFound("Post not found")

    post.delete()
    

def get_post_detail(user, post_id):
    post = get_post_by_id(post_id)
    
    if not post or post.owner != user:
        raise NotFound("Post not found")
    
    return post


def get_post_list(user_id=None, ordering='-created_at'):
    posts = post_list(
        user_id = user_id,
        ordering = ordering
    )
    
    return posts


def save_post(user, post):
    already_saved = is_post_saved(user, post)

    if already_saved:
        raise ValidationError("This post has already been saved.")

    return create_saved_post(user, post)


def create_saved_post(user, post):
    saved_post = SavedPost.objects.create(
        user=user,
        post=post
    )
    return saved_post
