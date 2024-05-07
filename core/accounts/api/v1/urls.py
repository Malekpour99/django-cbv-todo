from django.urls import path
from . import views

urlpatterns = [
    # Registration
    path("registration/", views.UserRegistration.as_view(), name="registration"),
    # Token
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
]
