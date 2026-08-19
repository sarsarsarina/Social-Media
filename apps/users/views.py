from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .services import create_user


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = create_user(serializer.validated_data)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            'access': str(access),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)

