from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .paginations import CommentListPagination
from .serializers import (
    CommentSerializer,
    CreateCommentSerializer,
    PostCommentSerializer,
    PostCommentsFilterSerializer,
    ReplySerializer,
    UpdateCommentSerializer,
)
from .services import (
    create_comment,
    delete_comment,
    get_comment_replies,
    get_post_comments,
    update_comment,
)
from drf_spectacular.utils import extend_schema


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CreateCommentSerializer,
        responses={201: CommentSerializer},
    )
    def post(self, request, post_id):
        serializer = CreateCommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        comment = create_comment(request.user, post_id, serializer.validated_data)

        response_serializer = CommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UpdateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UpdateCommentSerializer,
        responses={200: CommentSerializer},
    )
    def patch(self, request, comment_id):
        serializer = UpdateCommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        comment = update_comment(request.user, comment_id, serializer.validated_data)

        response_serializer = CommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        delete_comment(request.user, comment_id)

        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_200_OK)


class PostCommentsView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class  = CommentListPagination

    def get(self, request, post_id):
        filter_serializer = PostCommentsFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        comments = get_post_comments(post_id, ordering=filter_serializer.validated_data['ordering'],)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(comments, request, view=self)
        serializer = PostCommentSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class CommentRepliesView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CommentListPagination

    def get(self, request, comment_id):
        comment, replies = get_comment_replies(comment_id)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(replies, request)
        serializer = ReplySerializer(page, many=True)

        response = paginator.get_paginated_response(serializer.data)
        response.data['comment'] = CommentSerializer(comment).data

        return response
