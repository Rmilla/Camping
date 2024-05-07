from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=400)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid username or password."}, status=400)

        # Create a refresh token and access token
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })