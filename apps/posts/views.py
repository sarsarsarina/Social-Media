from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .selectors import my_posts
from .services import create_post
from .serializers import MyPostSerializer, CreatePostSerializer
from .paginations import PostListPagination
 
class MyPostsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        posts = my_posts(request.user)
        paginator = PostListPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = MyPostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    
    def post(self,request):
        serializer = CreatePostSerializer(data=request.data)
    
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        post = create_post(request.user, serializer.validated_data)

        response_serializer = MyPostSerializer(post)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    