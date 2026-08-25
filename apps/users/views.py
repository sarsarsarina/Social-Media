from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .services import create_user
from .serializers import RegisterSerializer, LoginSerializer
from .services import login_user

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