from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.


# 定义一个Inline类，使其纵向排列
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False  # 防止误删
    verbose_name_plural = "用户扩展信息"


# 重新注册User核心
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline, ]


# 注销源来的 User Admin
admin.site.unregister(User)
# 重新注册
admin.site.register(User, UserAdmin)





