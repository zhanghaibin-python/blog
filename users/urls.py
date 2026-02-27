from django.urls import path
from .views import RegisterAPIView, LoginAPIView, CurrentUserAPIView, LogoutAPIView

app_name = "users"

urlpatterns = [
    path('users/', RegisterAPIView.as_view(), name="register"),
    path('auth/login/', LoginAPIView.as_view(), name="login"),
    path('users/me/', CurrentUserAPIView.as_view(), name="me"),
    path('auth/logout/', LogoutAPIView.as_view(), name="logout")
]