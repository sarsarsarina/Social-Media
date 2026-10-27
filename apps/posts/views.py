from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import (
    my_posts,
    explore_posts,
    get_post_by_id,
)
from .services import (
    create_post,
    update_post,
    delete_post,
    get_post_detail,
    get_post_list,
    save_post,
    unsave_post,
    get_feed,
)
from .serializers import (
    MyPostSerializer,
    CreatePostSerializer,
    UpdatePostSerializer,
    PostDetailSerializer,
    FeedPostSerializer,
)
from .paginations import PostListPagination
from apps.users.paginations import StandardListPagination


class MyPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = my_posts(request.user)
        paginator = PostListPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = MyPostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = CreatePostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        post = create_post(request.user, serializer.validated_data)

        response_serializer = MyPostSerializer(post)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UpdatePostView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, post_id):
        serializer = UpdatePostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        post = update_post(request.user, post_id, serializer.validated_data)

        serializer = MyPostSerializer(instance=post)

        return Response(serializer.data)


class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        delete_post(request.user, post_id)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_post_detail(request.user, post_id)
        serializer = PostDetailSerializer(instance=post)

        return Response(serializer.data)


class PostListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PostListPagination

    def get(self, request):
        user_id = request.query_params.get('user_id')
        ordering = request.query_params.get('ordering', '-created_at')

        posts = get_post_list(
            user_id=user_id,
            ordering=ordering
        )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request)

        serializer = MyPostSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class ExploreView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = explore_posts()

        paginator = StandardListPagination()
        page = paginator.paginate_queryset(posts, request)

        serializer = PostDetailSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class SavedPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_post_by_id(post_id)

        if post is None:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        save_post(request.user, post)
        return Response({"message": "Post saved successfully."}, status=status.HTTP_201_CREATED)


class UnsavePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_post_by_id(post_id)

        if post is None:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        unsave_post(request.user, post)
        return Response({"message": "Post unsaved successfully."}, status=status.HTTP_200_OK)


class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PostListPagination

    def get(self, request):
        ordering = request.query_params.get('ordering', '-created_at')

        posts = get_feed(request.user, ordering)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request)
        serializer = FeedPostSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
