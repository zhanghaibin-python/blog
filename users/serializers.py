from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6
            }
        }

    def create(self, validated_data):

        # create_user 会触发 signal，自动创建 Profile
        user = User.objects.create_user(**validated_data)
        return user


# 用户资料修改：包含内嵌字段
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)    # 用户名通常不允许修改

    class Meta:
        model = UserProfile
        fields = [
            'nickname',
            'avatar', 'bio', 'username'
        ]




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)