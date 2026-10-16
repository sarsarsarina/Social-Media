from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import like_post, unlike_post
from .selectors import get_post_by_id, get_likes_list
from .serializers import LikeSerializer, PostLikesListSerializer
from apps.users.paginations import StandardListPagination


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_post_by_id(post_id)

        if post is None:
            return Response(
                {"message": "Post not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        like = like_post(request.user, post)
        serializer = LikeSerializer(instance=like)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_post_by_id(post_id)

        if post is None:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        unlike = unlike_post(request.user, post)
        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)


class PostLikesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_post_by_id(post_id)

        if post is None:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        likes_list = get_likes_list(post)
        paginator = StandardListPagination()
        page = paginator.paginate_queryset(likes_list, request)
        serializer = PostLikesListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
