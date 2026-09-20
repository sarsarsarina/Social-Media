from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .selectors import my_posts
from .serializers import MyPostSerializer
from .paginations import PostListPagination
 
class MyPostsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        posts = my_posts(request.user)
        paginator = PostListPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = MyPostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)