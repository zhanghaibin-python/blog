# util/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response

"""
在settings.py中：
# 注册自定义异常处理
    'EXCEPTION_HANDLER': 'util.exceptions.custom_exception_handler',
"""


def custom_exception_handler(exc, context):
    """
    自定义异常处理，捕获 DRF 默认处理不了的异常，或者统一修改异常返回格式
    """
    # 先调用 DRF 默认的异常处理
    response = exception_handler(exc, context)

    if response is not None:
        # 如果 DRF 已经处理了（比如 404, 401, 400），我们可以在这里进一步加工
        # 但因为我们在 Renderer 里也做了处理，这里主要用于处理 "非标准" 的异常结构
        # 或者记录日志
        pass
    else:
        # 处理 DRF 没捕获的异常（比如 500 服务器内部错误）
        # 在这里可以记录 error log
        return Response({
            'detail': f'Internal Server Error: {str(exc)}'
        }, status=500)

    return response