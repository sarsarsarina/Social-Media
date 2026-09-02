from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .services import create_user, logout_user, get_my_profile
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, MyProfileSerializer, UserProfileSerializer
from .services import login_user, get_user_profile
from rest_framework.permissions import IsAuthenticated

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
        return Response(data, status = status.HTTP_200_OK)
        

class MyProfileView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = get_my_profile(request.user.id)
        serializer = MyProfileSerializer(user)
        return Response(serializer.data)