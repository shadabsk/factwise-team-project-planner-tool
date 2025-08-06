from rest_framework import serializers

from django.conf import settings


class TeamCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=4, max_length=64)
    description = serializers.CharField(max_length=128)
    admin = serializers.CharField(max_length=8)

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


class AddUsersToTeamSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=8)
    users = serializers.ListField(
        child=serializers.CharField(max_length=8)
    )


class TeamIdSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=8)


class DescribeOrUpdateTeamSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=8)


class UpdateTeamPayloadSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=4, max_length=64)
    description = serializers.CharField(max_length=128)
    admin = serializers.CharField(max_length=8)


class UpdateTeamSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=8)
    team = UpdateTeamPayloadSerializer()


class RemoveUsersFromTeamSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=8)
    users = serializers.ListField(
        child=serializers.CharField(max_length=8),
        max_length=50
    )
