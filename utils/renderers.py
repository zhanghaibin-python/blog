from rest_framework.renderers import JSONRenderer
"""
只需在settings.py 中注册：
# 注册自定义渲染器
    'DEFAULT_RENDERER_CLASSES': (
        'utils.renderers.CustomJSONRenderer',  # 你的自定义 Renderer
        'rest_framework.renderers.BrowsableAPIRenderer', # 保留 API 页面
    ),
"""

class CustomJSONRenderer(JSONRenderer):
    """
    重写 render 方法，将所有接口的返回数据强制包装为 {code, msg, data} 格式
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 默认标准格式
        response_data = {
            'code': 200,
            'msg': 'success',
            'data': data
        }

        # 获取响应对象
        response = renderer_context.get('response')

        # 如果响应中有 error 字段，或者 status_code >= 400，说明是异常情况
        if response is not None and response.status_code >= 400:
            response_data['code'] = response.status_code
            response_data['msg'] = '请求处理失败'  # 默认提示
            
            # 如果 data 是 list 或 dict，通常包含具体的错误详情
            if isinstance(data, dict):
                # 1. 如果有 detail 字段（DRF 认证/权限异常通常会有这个）
                if 'detail' in data:
                    response_data['msg'] = data['detail']
                # 2. 如果是字段校验错误（key 是字段名，value 是错误列表）
                else:
                    # 尝试获取第一个错误的字段和信息
                    # 例如: {"password": ["密码太短"], "username": ["必填"]}
                    # 提取: "password: 密码太短"
                    for key, value in data.items():
                        if isinstance(value, list) and len(value) > 0:
                            response_data['msg'] = f"{key}: {value[0]}"
                            break
                        elif isinstance(value, str):
                            response_data['msg'] = value
                            break
                            
            elif isinstance(data, list) and len(data) > 0:
                # 处理列表类型的错误
                response_data['msg'] = str(data[0])

            # 处理 Validation Error 格式
            response_data['data'] = data

        return super().render(response_data, accepted_media_type, renderer_context)