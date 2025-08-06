from rest_framework import serializers

from django.conf import settings


class AddTaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=128)
    user_id = serializers.CharField(max_length=8)
    board_id = serializers.CharField(max_length=8)
    creation_time = serializers.CharField()

    def validate_title(self, value):
        board_id = self.initial_data.get("board_id")
        task_map = self.context.get("task_title_map", {})
        existing_titles = task_map.get(board_id, set())

        if value in existing_titles:
            raise serializers.ValidationError(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TASK_TITLE_UNIQUE']
            )
        return value


class TaskStatusUpdateSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=11)
    status = serializers.ChoiceField(choices=settings.TASK_STATUS_CHOICES)
