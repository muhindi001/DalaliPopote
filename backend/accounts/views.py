from rest_framework import generics
from rest_framework import parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer, EmailOrUsernameTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    parser_classes = [
        parsers.JSONParser,
        parsers.FormParser,
        parsers.MultiPartParser,
    ]


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = EmailOrUsernameTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)