from rest_framework import serializers

from django.conf import settings


class TeamCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=128)
    admin = serializers.CharField()

    def validate_name(self, value):
        existing_names = self.context.get("existing_team_names", [])
        if value in existing_names:
            raise serializers.ValidationError(
                settings.RESPONSE_MSG_CONSTANTS_DICT['TEAM_NAME_UNIQUE']
            )
        return value

    def validate_admin(self, value):
        existing_users = self.context.get("existing_user_ids", [])
        if value not in existing_users:
            raise serializers.ValidationError(
                settings.RESPONSE_MSG_CONSTANTS_DICT['ADMIN_NOT_EXIST']
            )
        return value


class TeamListSerializer(serializers.Serializer):
    team_id = serializers.CharField()
    team_name = serializers.CharField()
    description = serializers.CharField()
    creation_time = serializers.CharField()
    admin = serializers.CharField()


class AddUsersToTeamSerializer(serializers.Serializer):
    id = serializers.CharField()
    users = serializers.ListField(
        child=serializers.CharField(),
        max_length=50
    )


class TeamIdSerializer(serializers.Serializer):
    id = serializers.CharField()


class DescribeOrUpdateTeamSerializer(serializers.Serializer):
    id = serializers.CharField()


class UpdateTeamPayloadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=128)
    admin = serializers.CharField()


class UpdateTeamSerializer(serializers.Serializer):
    id = serializers.CharField()
    team = UpdateTeamPayloadSerializer()


class RemoveUsersFromTeamSerializer(serializers.Serializer):
    id = serializers.CharField()
    users = serializers.ListField(
        child=serializers.CharField(),
        max_length=50
    )
