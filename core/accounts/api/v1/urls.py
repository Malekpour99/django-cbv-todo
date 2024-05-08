from django.urls import path
from . import views

urlpatterns = [
    # Registration
    path("registration/", views.UserRegistration.as_view(), name="registration"),
    # Password Management
    path("change-password/", views.ChangePasswordAPIView.as_view(), name="change-password"),
    # Token
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    # JWT
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),

]
