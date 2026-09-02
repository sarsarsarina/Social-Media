from rest_framework.views import APIView
from .serializers import (RegisterSerializer, LoginSerializer, LogoutSerializer,
                          UpdateProfileSerializer, FollowUserSerializer)
from rest_framework.response import Response
from rest_framework import status
from .services import create_user, logout_user, login_user, update_profile, follow_user
from rest_framework.permissions import IsAuthenticated
from .selectors import get_user_profile


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

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = login_user(**serializer.validated_data)

        if data is None:
            return Response(
                {'error': 'اطلاعات ورود اشتباه است'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            logout_user(**serializer.validated_data)
        )


class UpdateProfileView(APIView):
    def patch(self, request):
        profile = get_user_profile(request.user)

        serializer = UpdateProfileSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updated_profile = update_profile(
            request.user,
            serializer.validated_data
        )


class FollowUserView(APIView):
    def post(self, request):
        serializer = FollowUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        following = validated_data['following']
        follower = request.user

        follow = follow_user(follower, following)

        serializer = FollowUserSerializer(instance=follow)
        return Response(serializer.data, status=status.HTTP_200_OK)
