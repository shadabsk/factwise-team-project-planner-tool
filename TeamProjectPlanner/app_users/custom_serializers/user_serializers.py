from rest_framework import serializers

from django.conf import settings

from common_utils import auth_utils as common_auth_utils


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    display_name = serializers.CharField(max_length=64)
    password = serializers.CharField(min_length=6, write_only=True)
    description = serializers.CharField(
        max_length=128, required=False, allow_blank=True
    )
    is_admin = serializers.BooleanField(required=False, default=False)

    def validate_name(self, value):
        existing_names = self.context.get("existing_names", [])
        if value in existing_names:
            raise serializers.ValidationError(
                settings.RESPONSE_MSG_CONSTANTS_DICT['UNAME_EXIST']
            )
        return value

    def validate_is_admin(self, value):
        existing_admins = self.context.get("existing_admins", [])
        if value is True and existing_admins:
            raise serializers.ValidationError(
                settings.RESPONSE_MSG_CONSTANTS_DICT['ADMIN_EXIST']
            )
        return value

    def create(self, validated_data):
        validated_data["password"] = common_auth_utils.hash_password(
            validated_data["password"]
        )
        return validated_data


class UserIdSerializer(serializers.Serializer):
    id = serializers.CharField()


class UpdateUserSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(required=False)
    display_name = serializers.CharField(required=False)
