from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .paginations import CommentListPagination
from .serializers import (
    CommentSerializer, 
    CreateCommentSerializer, 
    UpdateCommentSerializer,
    PostCommentsFilterSerializer,
    PostCommentSerializer,
    )
from .services import create_comment, update_comment, delete_comment, get_post_comments


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        serializer = CreateCommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        comment = create_comment(request.user, post_id, serializer.validated_data)

        response_serializer = CommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UpdateCommentView(APIView):
    permission_classes = [IsAuthenticated]

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
    parser_classes = CommentListPagination

    def get(self, request, post_id):
        filter_serializer = PostCommentsFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        comments = get_post_comments(post_id, ordering=filter_serializer.validated_data['ordering'],)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(comments, request, view=self)
        serializer = PostCommentSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
