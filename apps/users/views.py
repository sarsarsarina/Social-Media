from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .services import create_user
from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = create_user(serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
     
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
         
        if email:
            user = User.objects.filter(email = email).first()
            if user:
                user = authenticate(
                    username = username,
                    password = password
                )
        
        elif username:
            user = authenticate(
                username = username,
                password = password
            )
        else:
            user = None
            
        if user is None:
            return Response('اطلاعات ورود اشتباه است')

        else:
            return Response('ورود موفق')
    
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
    
            return Response({
            "access": str(access),
            "refresh": str(refresh),
            })