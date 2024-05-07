from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404


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
