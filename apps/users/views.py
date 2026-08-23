from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .services import create_user
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
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
         
        user = login_user(
            email = email,
            username = username,
            password = password,
        )
        
        if user is None:
            return Response ('اطلاعات ورود اشتباه است', status = status.HTTP_401_UNAUTHORIZED)
        
        else:
            return Response(user)
            
        