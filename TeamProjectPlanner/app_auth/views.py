import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_auth import service as app_auth_service


class LoginAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_manager = app_auth_service.LoginManager()

    def post(self, request):
        try:
            result = self.login_manager.login(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED
            )
