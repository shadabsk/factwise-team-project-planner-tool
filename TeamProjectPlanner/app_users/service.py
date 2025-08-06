import json
from datetime import datetime
from uuid import uuid4

from django.conf import settings

from app_users.custom_serializers import user_serializers as \
    app_user_serializers

from project_planner_tool.base_interface import \
    user_base as user_base_interface

from common_utils import base_utils as generic_utils


class UserManager(user_base_interface.UserBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_user(self, request):
        data = json.loads(request)
        users_info = generic_utils.load_json(settings.USER_FILE)
        existing_names = {
            user["name"] for user in users_info
        }
        existing_admins = [
            user for user in users_info if user.get("is_admin")
        ]

        serializer = app_user_serializers.UserCreateSerializer(
            data=data,
            context={
                "existing_names": existing_names,
                "existing_admins": existing_admins
            }
        )
        serializer.is_valid(raise_exception=True)
        validated = serializer.save()

        user_id = "u_" + uuid4().hex[:6]

        new_user = {
            "user_id": user_id,
            "name": validated["name"],
            "display_name": validated["display_name"],
            "description": validated.get("description", ""),
            "creation_time": datetime.now().isoformat(),
            "is_admin": validated.get("is_admin", False),
            "password": validated["password"]
        }

        users_info.append(new_user)
        generic_utils.save_json(settings.USER_FILE, users_info)

        return json.dumps({"id": user_id})

    def list_users(self):
        users_info = generic_utils.load_json(settings.USER_FILE)
        return json.dumps(users_info)

    def describe_user(self, request, acting_user_id, is_admin):
        data = json.loads(request)
        serializer = app_user_serializers.UserIdSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["id"]

        users_info = generic_utils.load_json(settings.USER_FILE)
        user_record = next(
            (
                user for user in users_info if user["user_id"] == user_id
            ),
            None
        )
        if not user_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['USER_NOT_FOUND']
            )

        if user_id != acting_user_id and (not is_admin):
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['DENY']
            )

        return json.dumps(user_record)

    def update_user(self, request, acting_user_id, is_admin):
        data = json.loads(request)
        serializer = app_user_serializers.UpdateUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        users_info = generic_utils.load_json(settings.USER_FILE)
        user_record = next(
            (
                user for user in users_info
                if user["user_id"] == validated["id"]
            ),
            None
        )
        if not user_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['USER_NOT_FOUND']
            )

        # Only admin or the user themself can update
        if not (is_admin or validated["id"] == acting_user_id):
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['DENY']
            )

        if user_record["name"] != validated["name"]:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['USER_NAME_RESTRICT']
            )

        if "display_name" in validated:
            user_record["display_name"] = validated["display_name"]

        generic_utils.save_json(settings.USER_FILE, users_info)
        return json.dumps({"message": "User updated"})

    def get_user_teams(self, request, acting_user_id, is_admin):
        data = json.loads(request)
        serializer = app_user_serializers.UserIdSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["id"]

        # Only self or admin
        if not (is_admin or acting_user_id == user_id):
            raise Exception(settings.RESPONSE_MSG_CONSTANTS_DICT['DENY'])

        teams_info = generic_utils.load_json(settings.TEAM_FILE)

        user_teams = [
            {
                "id": team["team_id"],
                "name": team["team_name"]
            }
            for team in teams_info if user_id in team["members"]
        ]
        return json.dumps(user_teams)
