from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import like_post, unlike_post
from .selectors import get_post_by_id
from .serializers import LikeSerializer


class LikePost(APIView):
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


class UnlikePost(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_post_by_id(post_id)

        if post is None:
            return Response(
                {"message": "Post not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        unlike = unlike_post(request.user, post)
        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)