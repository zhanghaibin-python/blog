from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    # 注册信号
    def ready(self):
        # 导入信号，使其生效
        import users.signals

        # 导入 SimpleJWT 的模型
        try:
            from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

            # 动态修改“白名单/未完成 Token”表在后台的显示
            OutstandingToken._meta.verbose_name = _("已签发 Token")
            OutstandingToken._meta.verbose_name_plural = _("已签发 Token 列表")

            # 动态修改“黑名单”表在后台的显示
            BlacklistedToken._meta.verbose_name = _("黑名单 Token")
            BlacklistedToken._meta.verbose_name_plural = _("黑名单 Token 列表")
        except ImportError:
            pass
