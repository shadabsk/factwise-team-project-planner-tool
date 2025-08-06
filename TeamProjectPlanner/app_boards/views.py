import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from app_boards import service as boards_service

from common_utils import auth_utils as common_auth_utils


class CreateBoardAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boards_manager = boards_service.BoardsManager()

    def post(self, request):
        try:
            auth_header = request.headers.get("Authorization", "")
            token = auth_header.replace("Token ", "").strip()
            user = common_auth_utils.get_user_from_token(token)

            if not user:
                return Response(
                    {
                        "error": settings.RESPONSE_MSG_CONSTANTS_DICT['UNAUTH']
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            if not user.get("is_admin"):
                return Response(
                    {
                        "error": settings.RESPONSE_MSG_CONSTANTS_DICT[
                            'ONLY_ADMIN_RESTRICT_BOARDS'
                        ]
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            result = self.boards_manager.create_board(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ListBoardsAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boards_manager = boards_service.BoardsManager()

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

            result = self.boards_manager.list_boards(
                json.dumps({'id': team_id}),
                acting_user_id=user['user_id'],
                is_admin=user.get('is_admin', False)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class CloseBoardAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boards_manager = boards_service.BoardsManager()

    def post(self, request):
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

            result = self.boards_manager.close_board(
                json.dumps(request.data),
                acting_user_id=user['user_id'],
                is_admin=user.get('is_admin', False)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ExportBoardAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boards_manager = boards_service.BoardsManager()

    def post(self, request):
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

            result = self.boards_manager.export_board(
                json.dumps(request.data),
                acting_user_id=user['user_id'],
                is_admin=user.get('is_admin', False)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AddTaskAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = boards_service.TaskManager()

    def post(self, request):
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

        try:
            result = self.task_manager.add_task(
                json.dumps(request.data),
                acting_user_id=user["user_id"],
                is_admin=user.get('is_admin', False)
            )
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UpdateTaskStatusAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = boards_service.TaskManager()

    def put(self, request):
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

            result = self.task_manager.update_task_status(
                json.dumps(request.data),
                acting_user_id=user['user_id'],
                is_admin=user.get('is_admin', False)
            )
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
