import json
import os
from datetime import datetime
from uuid import uuid4

from django.conf import settings

from app_boards.custom_serializers import boards_serializer as \
    app_boards_serializer
from app_boards.custom_serializers import tasks_serializer as \
    app_tasks_serializer

from project_planner_tool.base_interface import project_board_base as \
    board_nd_task_base_interface

from common_utils import base_utils as generic_utils


class BoardsManager(board_nd_task_base_interface.ProjectBoardBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_board(self, request):
        data = json.loads(request)
        boards_info = generic_utils.load_json(settings.BOARD_FILE)
        teams_info = generic_utils.load_json(settings.TEAM_FILE)

        # Build team_id -> set(board_name) map
        team_board_map = {}
        for board in boards_info:
            team_board_map.setdefault(
                board["team_id"], set()
            ).add(board["name"])

        serializer = app_boards_serializer.BoardCreateSerializer(
            data=data,
            context={"team_board_map": team_board_map}
        )
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        team_record = next(
            (
                team for team in teams_info
                if team["team_id"] == validated["team_id"]
            ),
            None
        )
        if not team_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TEAM_NOT_FOUND']
            )

        board_id = "b_" + uuid4().hex[:6]
        new_board = {
            "board_id": board_id,
            "name": validated["name"],
            "description": validated["description"],
            "team_id": validated["team_id"],
            "creation_time": validated["creation_time"],
            # NOTE: Initializing with OPEN
            "status": settings.TASK_STATUS_CHOICES[0]
        }

        boards_info.append(new_board)
        generic_utils.save_json(settings.BOARD_FILE, boards_info)

        return json.dumps({"id": board_id})

    def list_boards(self, request):
        data = json.loads(request)
        team_id = data.get("id")
        boards_info = generic_utils.load_json(settings.BOARD_FILE)

        filtered = [
            {
                "id": board["board_id"],
                "name": board["name"],
                "status": board["status"]
            }
            for board in boards_info
            if board["team_id"] == team_id and board["status"]
        ]
        return json.dumps(filtered)

    def close_board(self, request):
        data = json.loads(request)
        serializer = app_boards_serializer.BoardIdSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        board_id = serializer.validated_data["id"]
        boards_info = generic_utils.load_json(settings.BOARD_FILE)
        tasks_info = generic_utils.load_json(settings.TASK_FILE)

        board_record = next(
            (
                board for board in boards_info
                if board["board_id"] == board_id
            ),
            None
        )
        if not board_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['BOARD_NOT_FOUND']
            )

        # BOARD_STATUS_CHOICES[-1] -> Closed
        if board_record["status"] == settings.BOARD_STATUS_CHOICES[-1]:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['BOARD_CLOSED']
            )

        incomplete_tasks = [
            task for task in tasks_info
            if task["board_id"] == board_id and task["status"] != "COMPLETE"
        ]
        if incomplete_tasks:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['BOARD_NOT_CLOSED']
            )

        board_record["status"] = "CLOSED"
        board_record["end_time"] = datetime.now().isoformat()
        generic_utils.save_json(settings.BOARD_FILE, boards_info)

        return json.dumps({"message": "Board closed successfully"})

    def export_board(self, request):
        data = json.loads(request)
        serializer = app_boards_serializer.BoardIdSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        board_id = serializer.validated_data["id"]

        boards_info = generic_utils.load_json(settings.BOARD_FILE)
        tasks_info = generic_utils.load_json(settings.TASK_FILE)
        users_info = generic_utils.load_json(settings.USER_FILE)

        board_record = next(
            (
                board for board in boards_info
                if board["board_id"] == board_id
            ),
            None
        )
        if not board_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['BOARD_NOT_FOUND']
            )

        board_tasks = [
            task for task in tasks_info
            if task["board_id"] == board_id
        ]
        user_map = {
            user["user_id"]: user["display_name"]
            for user in users_info
        }

        lines = [
            f"Board: {board_record['name']}",
            f"Description: {board_record['description']}",
            f"Created on: {board_record['creation_time']}",
            f"Status: {board_record['status']}",
            "-"*40,
            "Tasks:"
        ]
        for board_task in board_tasks:
            lines.extend([
                f"  • Title: {board_task['title']}",
                f"    Assigned to: {
                        user_map.get(
                            board_task['user_id'], 'Unknown'
                        )
                }",
                f"    Status: {board_task['status']}",
                f"    Created: {board_task['creation_time']}",
                ""
            ])

        os.makedirs(settings.EXPORT_DIR, exist_ok=True)
        filename = f"{settings.EXPORT_DIR}/{board_id}_summary.txt"

        with open(filename, "w") as f:
            f.write("\n".join(lines))

        return json.dumps({"out_file": filename})


class TaskManager(board_nd_task_base_interface.ProjectBoardBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_task(self, request, acting_user_id):
        data = json.loads(request)

        tasks_info = generic_utils.load_json(settings.TASK_FILE)
        boards_info = generic_utils.load_json(settings.BOARD_FILE)
        # users_info = generic_utils.load_json(settings.USER_FILE)
        teams_info = generic_utils.load_json(settings.TEAM_FILE)

        # Build: board_id → set(task_title)
        task_title_map = {}
        for task in tasks_info:
            task_title_map.setdefault(
                task["board_id"], set()
            ).add(task["title"])

        serializer = app_tasks_serializer.AddTaskSerializer(
            data=data,
            context={"task_title_map": task_title_map}
        )
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        # Validate board existence
        board_record = next(
            (
                board for board in boards_info
                if board["board_id"] == validated["board_id"]
            ),
            None
        )
        if not board_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['BOARD_NOT_FOUND']
            )

        # TASK_STATUS_CHOICES[0] -> OPEN
        if board_record["status"] != settings.TASK_STATUS_CHOICES[0]:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TASK_CANT_ADD']
            )

        # Check acting user (from token) is a member of board's team
        team_record = next(
            (
                team for team in teams_info
                if team["team_id"] == board_record["team_id"]
            ),
            None
        )
        if not team_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TEAM_NOT_FOUND_IN_BOARD']
            )

        if acting_user_id not in team_record["members"]:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['USER_NOT_IN_TEAM']
            )

        # Validate assigned user is also in the team
        if validated["user_id"] not in team_record["members"]:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT[
                    'ASSIGNED_USER_NOT_IN_TEAM'
                ]
            )

        task_id = "task_" + uuid4().hex[:6]
        new_task = {
            "task_id": task_id,
            "board_id": validated["board_id"],
            "title": validated["title"],
            "description": validated["description"],
            "user_id": validated["user_id"],
            "creation_time": validated["creation_time"],
            "status": "OPEN"
        }

        tasks_info.append(new_task)
        generic_utils.save_json(settings.TASK_FILE, tasks_info)

        return json.dumps({"id": task_id})

    def update_task_status(self, request: str) -> str:
        data = json.loads(request)
        serializer = app_tasks_serializer.TaskStatusUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        tasks_info = generic_utils.load_json(settings.TASK_FILE)
        task_record = next(
            (
                task for task in tasks_info
                if task["task_id"] == validated["id"]
            ),
            None
        )
        if not task_record:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TASK_NOT_FOUND']
            )

        task_record["status"] = validated["status"]
        generic_utils.save_json(settings.TASK_FILE, tasks_info)

        return json.dumps({"message": "Task status updated"})
