import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from app_users import service as user_service

from common_utils import auth_utils as common_auth_utils
from common_utils import base_utils as generic_utils


class CreateUserAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = user_service.UserManager()

    def post(self, request):
        try:
            result = self.user_manager.create_user(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ListUsersAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = user_service.UserManager()

    def get(self, request):
        token = request.headers.get(
            "Authorization", ""
        ).replace("Token ", "").strip()
        user = common_auth_utils.get_user_from_token(token)

        if not user or not user.get("is_admin"):
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT['UNAUTH']
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            result = self.user_manager.list_users()
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class DescribeUserAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = user_service.UserManager()

    def get(self, request):
        try:
            user_id = request.query_params.get("id")

            if not user_id:
                return Response(
                    {
                        "error": settings.RESPONSE_MSG_CONSTANTS_DICT[
                            'ID_PARAM_MISSING'
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = request.headers.get(
                "Authorization", ""
            ).replace("Token ", "").strip()
            user = common_auth_utils.get_user_from_token(token)

            if not user:
                return Response(
                    {
                        "error": settings.RESPONSE_MSG_CONSTANTS_DICT['UNAUTH']
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            result = self.user_manager.describe_user(
                json.dumps({"id": user_id}),
                acting_user_id=user['user_id'],
                is_admin=user.get('is_admin', False)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UpdateUserAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = user_service.UserManager()

    def put(self, request):
        token = request.headers.get("Authorization", "").replace("Token ", "")
        user = common_auth_utils.get_user_from_token(token)

        if not user:
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT['UNAUTH']
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            result = self.user_manager.update_user(
                json.dumps(request.data),
                acting_user_id=user["user_id"],
                is_admin=user.get("is_admin", False)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class GetUserTeamsAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = user_service.UserManager()

    def get(self, request):
        token = request.headers.get("Authorization", "").replace("Token ", "")
        user = common_auth_utils.get_user_from_token(token)

        if not user:
            return Response(
                {"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.query_params.get("id")

        if not user_id:
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT[
                        'ID_PARAM_MISSING'
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = self.user_manager.get_user_teams(
                json.dumps({"id": user_id}),
                acting_user_id=user["user_id"],
                is_admin=user.get("is_admin", False)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
