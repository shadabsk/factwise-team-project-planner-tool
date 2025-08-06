import json
from datetime import datetime
from uuid import uuid4

from django.conf import settings

from app_teams.custom_serializers import teams_serializer as \
    app_teams_serializer

from project_planner_tool.base_interface import team_base as \
    team_base_interface

from common_utils import base_utils as generic_utils


class TeamsManager(team_base_interface.TeamBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_team(self, request):
        data = json.loads(request)

        teams_info = generic_utils.load_json(settings.TEAM_FILE)
        users_info = generic_utils.load_json(settings.USER_FILE)

        existing_team_names = {team["team_name"] for team in teams_info}
        existing_user_ids = {user["user_id"] for user in users_info}

        serializer = app_teams_serializer.TeamCreateSerializer(
            data=data,
            context={
                "existing_team_names": existing_team_names,
                "existing_user_ids": existing_user_ids
            }
        )
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        team_id = "t_" + uuid4().hex[:6]
        creation_time = datetime.now().isoformat()

        new_team = {
            "team_id": team_id,
            "team_name": validated["name"],
            "description": validated["description"],
            "creation_time": creation_time,
            "admin": validated["admin"],
            "created_by": validated["admin"],
            "members": [validated["admin"]]
        }

        teams_info.append(new_team)
        generic_utils.save_json(settings.TEAM_FILE, teams_info)

        return json.dumps({"id": team_id})

    def list_teams(self):
        teams = generic_utils.load_json(settings.TEAM_FILE)
        return json.dumps(teams)

    def add_users_to_team(self, request):
        data = json.loads(request)
        serializer = app_teams_serializer.AddUsersToTeamSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        team_id = validated["id"]
        users_to_add = validated["users"]

        teams_info = generic_utils.load_json(settings.TEAM_FILE)
        users_info = generic_utils.load_json(settings.USER_FILE)

        team_record = next(
            (team for team in teams_info if team["team_id"] == team_id),
            None
        )
        if not team_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TEAM_NOT_FOUND']
            )

        # Validate all user_ids
        user_ids = {user["user_id"] for user in users_info}
        for uid in users_to_add:
            if uid not in user_ids:
                raise Exception(
                    settings.RESPONSE_MSG_CONSTANTS_DICT[
                        'USER_NOT_EXIST'
                    ].format(uid)
                )

        team_record["members"] = list(
            set(team_record["members"]) | set(users_to_add)
        )

        generic_utils.save_json(settings.TEAM_FILE, teams_info)
        return json.dumps({"message": "Users added successfully"})

    def list_team_users(self, request, acting_user_id, is_admin):
        data = json.loads(request)
        serializer = app_teams_serializer.TeamIdSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        team_id = serializer.validated_data["id"]

        teams_info = generic_utils.load_json(settings.TEAM_FILE)
        users_info = generic_utils.load_json(settings.USER_FILE)

        team_record = next(
            (team for team in teams_info if team["team_id"] == team_id),
            None
        )
        if not team_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TEAM_NOT_FOUND']
            )
        if not is_admin and acting_user_id not in team_record['members']:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['DENY']
            )

        team_members = [
            user for user in users_info
            if user["user_id"] in team_record["members"]
        ]
        result = [
            {
                "user_id": user["user_id"],
                "name": user["name"],
                "display_name": user["display_name"]
            }
            for user in team_members
        ]
        return json.dumps(result)

    def describe_team(self, request, acting_user_id, is_admin):
        data = json.loads(request)
        serializer = app_teams_serializer.DescribeOrUpdateTeamSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)

        team_id = serializer.validated_data["id"]
        teams_info = generic_utils.load_json(settings.TEAM_FILE)
        team_record = next(
            (team for team in teams_info if team["team_id"] == team_id),
            None
        )
        if not team_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TEAM_NOT_FOUND']
            )
        if not is_admin and acting_user_id not in team_record['members']:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['DENY']
            )
        return json.dumps(team_record)

    def update_team(self, request):
        data = json.loads(request)
        serializer = app_teams_serializer.UpdateTeamSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        team_id = serializer.validated_data["id"]
        updated_data = serializer.validated_data["team"]

        teams_info = generic_utils.load_json(settings.TEAM_FILE)
        users_info = generic_utils.load_json(settings.USER_FILE)

        team_record = next(
            (team for team in teams_info if team["team_id"] == team_id),
            None
        )
        if not team_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TEAM_NOT_FOUND']
            )

        existing_names = {
            team["team_name"]
            for team in teams_info if team["team_id"] != team_id
        }
        user_ids = {user["user_id"] for user in users_info}

        if updated_data["name"] in existing_names:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['UNIQUE_TEAM_NAME']
            )

        if updated_data["admin"] not in user_ids:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['ADMIN_NOT_EXIST']
            )

        team_record["team_name"] = updated_data["name"]
        team_record["description"] = updated_data["description"]
        team_record["admin"] = updated_data["admin"]
        generic_utils.save_json(settings.TEAM_FILE, teams_info)
        return json.dumps({"message": "Team updated successfully"})

    def remove_users_from_team(self, request):
        data = json.loads(request)
        serializer = app_teams_serializer.RemoveUsersFromTeamSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)

        team_id = serializer.validated_data["id"]
        remove_ids = set(serializer.validated_data["users"])

        teams_info = generic_utils.load_json(settings.TEAM_FILE)
        users_info = generic_utils.load_json(settings.USER_FILE)

        team_record = next(
            (team for team in teams_info if team["team_id"] == team_id),
            None
        )
        if not team_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TEAM_NOT_FOUND']
            )

        user_ids = {user["user_id"] for user in users_info}
        for user_to_remove_id in remove_ids:
            if user_to_remove_id not in user_ids:
                raise Exception(
                    settings.RESPONSE_MSG_CONSTANTS_DICT[
                        'USER_NOT_EXIST'
                    ].format(user_to_remove_id)
                )
            if user_to_remove_id not in team_record['members']:
                raise Exception(settings.RESPONSE_MSG_CONSTANTS_DICT['UNAUTH'])

        team_record["members"] = [
            user_id
            for user_id in team_record["members"] if user_id not in remove_ids
        ]
        generic_utils.save_json(settings.TEAM_FILE, teams_info)
        return json.dumps({"message": "Users removed from team"})
