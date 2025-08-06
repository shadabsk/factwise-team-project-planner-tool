from rest_framework import serializers

from django.conf import settings


class BoardCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=4, max_length=64)
    description = serializers.CharField(min_length=4, max_length=128)
    team_id = serializers.CharField(max_length=8)
    creation_time = serializers.CharField()

    def validate_name(self, value):
        # Context should contain existing board names per team
        team_id = self.initial_data.get("team_id")
        team_board_map = self.context.get("team_board_map", {})

        existing_names = team_board_map.get(team_id, set())
        if value in existing_names:
            raise serializers.ValidationError(
                settings.RESPONSE_MSG_CONSTANTS_DICT['UNIQUE_BOARD']
            )
        return value


class BoardIdSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=8)
