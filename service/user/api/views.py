from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import *


# Create your views here.
class RegisterView(APIView):
    """Endpoint to register a new user"""
    def post(self, request):
        """Get posted registration data"""
        serializer = RegistrationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            account = serializer.save()
            refresh = RefreshToken.for_user(account)

            data = {
                'response': 'Registration successful',
                'username': account.username,
                'email': account.email,
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Endpoint to log in a user"""
    def post(self, request):
        """Login request"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        data = {
            'response': 'Loging successful',
            'username': RegistrationSerializer(user).data.get('username'),
            'email': RegistrationSerializer(user).data.get('email'),
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Endpoint to log out a user"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout request"""
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
