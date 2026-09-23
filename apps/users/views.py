from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiRequest

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
    FollowRequestSerializer,
    BlockUserSerializer,
    BlockListSerializer
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
    block_user,
    get_followers_count,
    get_following_count,
    get_user_profile,
    get_user_by_id,
    restrict_user,
    unrestrict_user,
    unblock_user,
)

from .selectors import get_profile_by_user, followers_list, following_list, block_list
from .paginations import FollowersListPagination, BlockListPagination

@extend_schema(request=RegisterSerializer)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = create_user(serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED)

@extend_schema(request=LoginSerializer)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = login_user(**serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)

@extend_schema(request=LogoutSerializer)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = logout_user(**serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)

@extend_schema(request=UpdateProfileSerializer)
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
        profile = get_user_profile(user_id, request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

@extend_schema(request=FollowUserSerializer)
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

    def delete(self, request, user_id):
        following = get_user_by_id(user_id)

        if following is None:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        unfollow_user(request.user, following)

        return Response(
            {"message": "User unfollowed successfully."},
            status=status.HTTP_200_OK
        )


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


@extend_schema(request=FollowRequestSerializer)
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


class UserFollowersCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        count = get_followers_count(user_id)

        return Response({'followers_count': count}, status=status.HTTP_200_OK)


class UserFollowingCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        count = get_following_count(user_id)

        return Response({'following_count': count}, status=status.HTTP_200_OK)
    
    
@extend_schema(request=BlockUserSerializer)
class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BlockUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        blocked = validated_data['blocked']
        blocker = request.user

        block_user(blocker, blocked)

        return Response({"message": "User blocked successfully."}, status=status.HTTP_200_OK)


class RestrictUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        restricted_user = get_user_by_id(user_id)

        if restricted_user is None:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        restrict_user(request.user, restricted_user)

        return Response({"message": "This user is restricted."}, status=status.HTTP_200_OK)


class UnrestrictUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        restricted_user = get_user_by_id(user_id)

        if restricted_user is None:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        unrestrict_user(request.user, restricted_user)

        return Response({"message": "User unrestricted successfully."}, status=status.HTTP_200_OK)


class UnblockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = BlockUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        blocked = validated_data['blocked']

        unblock_user(request.user, blocked)

        return Response({"message": "User unblocked successfully."}, status=status.HTTP_200_OK)


class BlockListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blocks = block_list(request.user)
        paginator = BlockListPagination()
        page = paginator.paginate_queryset(blocks, request)
        serializer = BlockListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
