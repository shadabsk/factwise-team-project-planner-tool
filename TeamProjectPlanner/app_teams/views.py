import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from app_teams import service as teams_service

from common_utils import auth_utils as common_auth_utils
from common_utils import base_utils as generic_utils


class CreateTeamAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teams_manager = teams_service.TeamsManager()

    def post(self, request):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Token ", "").strip()
        user = common_auth_utils.get_user_from_token(token)

        if not user or not user.get("is_admin"):
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT[
                        'ONLY_ADMIN_RESTRICT_TEAM'
                    ]
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            result = self.teams_manager.create_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ListTeamsAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teams_manager = teams_service.TeamsManager()

    def get(self, request):
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

        if not user["is_admin"]:
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT['DENY']
                },
                status=status.HTTP_403_FORBIDDEN
            )

        result = self.teams_manager.list_teams()
        return Response(json.loads(result), status=status.HTTP_200_OK)


class AddUsersToTeamAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teams_manager = teams_service.TeamsManager()

    def put(self, request):
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

        if not user["is_admin"]:
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT['DENY']
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            result = self.teams_manager.add_users_to_team(
                json.dumps(request.data)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ListTeamUsersAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teams_manager = teams_service.TeamsManager()

    def get(self, request):
        try:
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

            team_id = request.query_params.get("id")

            if not team_id:
                return Response(
                    {
                        "error": settings.RESPONSE_MSG_CONSTANTS_DICT[
                            'ID_PARAM_MISSING'
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = self.teams_manager.list_team_users(
                json.dumps({"id": team_id}),
                acting_user_id=user['user_id'],
                is_admin=user.get('is_admin', False)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class DescribeTeamAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teams_manager = teams_service.TeamsManager()

    def get(self, request):
        try:
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

            team_id = request.query_params.get("id")

            if not team_id:
                return Response(
                    {
                        "error": settings.RESPONSE_MSG_CONSTANTS_DICT[
                            'ID_PARAM_MISSING'
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = self.teams_manager.describe_team(
                json.dumps({"id": team_id}),
                acting_user_id=user['user_id'],
                is_admin=user.get('is_admin', False)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UpdateTeamAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teams_manager = teams_service.TeamsManager()

    def put(self, request):
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
        if not user['is_admin']:
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT['DENY']
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            result = self.teams_manager.update_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class RemoveUsersFromTeamAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teams_manager = teams_service.TeamsManager()

    def delete(self, request):
        team_id = request.query_params.get("id")

        if not team_id:
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT[
                        'ID_PARAM_MISSING'
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_to_remove_ids = request.query_params.get("users")

        if not user_to_remove_ids:
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT[
                        'USER_PARAM_MISSING'
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user_to_remove_ids = (
            user_to_remove_ids.split(",") if user_to_remove_ids else []
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
        if not user['is_admin']:
            return Response(
                {
                    "error": settings.RESPONSE_MSG_CONSTANTS_DICT['DENY']
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            result = self.teams_manager.remove_users_from_team(
                json.dumps({'id': team_id, 'users': user_to_remove_ids})
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
