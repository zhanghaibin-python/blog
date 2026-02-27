from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class RegisterAPIView(APIView):
    """
    注册视图API
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'message': '注册成功'},
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    """
    登录视图API
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({
                "detail": '用户名或密码错误! '
            }, status=status.HTTP_400_BAD_REQUEST)

        # 生成 token
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": '登录成功! ',
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)



class CurrentUserAPIView(APIView):
    """
    返回当前用户信息
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({
                "message": "用户未登录! "
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "username": request.user.username
        })


class LogoutAPIView(APIView):
    def post(self, request):
       try:
           refresh_token = request.data["refresh"]
           token = RefreshToken(refresh_token)
           # 将该 refresh token 加入黑名单
           token.blacklist()
           return Response({
               "detail": "Successfully logged out."
           }, status=status.HTTP_200_OK)
       except Exception:
           return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)












