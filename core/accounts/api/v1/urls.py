from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.UserRegistration.as_view(), name="registration"),
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
]
