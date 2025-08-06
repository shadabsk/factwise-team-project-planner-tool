from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=4, max_length=64)
    password = serializers.CharField(min_length=4)
