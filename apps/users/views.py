from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    UpdateProfileSerializer,
    FollowUserSerializer,
    MyProfileSerializer,
    UserProfileSerializer,
    FollowersListSerializer,
    FollowingListSerializer,
    FollowRequestSerializer
)

from .services import (
    create_user,
    logout_user,
    login_user,
    update_profile,
    follow_user,
    get_my_profile,
    unfollow_user,
    follow_request,
)

from .selectors import get_profile_by_user, followers_list, following_list
from . paginations import FollowersListPagination


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = create_user(serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = login_user(**serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = logout_user(**serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UpdateProfileSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updated_profile = update_profile(
            request.user,
            serializer.validated_data
        )

        serializer = UserProfileSerializer(instance=updated_profile)
        return Response(serializer.data)


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_my_profile(request.user.id)
        serializer = MyProfileSerializer(user)
        return Response(serializer.data)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        profile = get_profile_by_user(user_id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FollowUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        following = validated_data['following']
        follower = request.user

        follow_user(follower, following)

        return Response({"message": "User followed successfully."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = FollowUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        following = validated_data['following']

        unfollow_user(request.user, following)

        return Response({"message": "User unfollowed successfully."}, status.HTTP_200_OK)


class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followers = followers_list(request.user)
        paginator = FollowersListPagination()
        page = paginator.paginate_queryset(followers, request)
        serializer = FollowersListSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following = following_list(request.user)
        paginator = FollowersListPagination()
        page = paginator.paginate_queryset(following, request)
        serializer = FollowingListSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class FollowRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FollowRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        to_user = validated_data['to_user']
        from_user = request.user
        follow_request(from_user, to_user)

        return Response({"message": "Follow request sent successfully."}, status=status.HTTP_200_OK)