from rest_framework.response import Response

def success(data=None, message="success", code=200, status=200):
    return Response({
        "code": code,
        "message": message,
        "data": data
    }, status=status)


def error(message="error", code=400, data=None, status=400):
    return Response({
        "code": code,
        "message": message,
        "data": data
    }, status=status)