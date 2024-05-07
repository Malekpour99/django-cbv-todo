from rest_framework.response import Response
from .serializers import RegistrationSerializer, CustomAuthTokenSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class UserRegistration(GenericAPIView):
    """Registration for users"""

    serializer_class = RegistrationSerializer

    def post(self, request):
        """Create a new user from provided data"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data["email"]
        data = {"email": email}
        # Prevention of receiving hashed password in the serializer.data
        return Response(data, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})
