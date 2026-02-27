from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    封装自定义权限
    """
    def has_object_permission(self, request, view, obj):
        # 允许 GET, HEAD, OPTIONS 请求（读取权限）
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写入权限只给作者
        return obj.author == request.user