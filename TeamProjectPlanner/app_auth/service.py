import json
from datetime import datetime

from django.conf import settings

from app_auth.custom_serializers import auth_serializer as app_auth_serializer

from common_utils import auth_utils as common_auth_utils
from common_utils import base_utils as generic_utils


class LoginManager:
    def login(self, request):
        data = json.loads(request)
        serializer = app_auth_serializer.LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        users = generic_utils.load_json(settings.USER_FILE)
        matched_user = None
        for user in users:
            if user["name"] == validated["name"]:
                if user["password"] == common_auth_utils.hash_password(
                    validated["password"]
                ):
                    matched_user = user
                    break

        if not matched_user:
            raise Exception(
                settings.RESPONSE_MSG_CONSTANTS_DICT['INVALID_CRED']
            )

        # Generate and store token
        generated_token = common_auth_utils.generate_token(
            matched_user["user_id"]
        )
        tokens_info = generic_utils.load_json(settings.TOKEN_FILE)

        # delete old token for user establishing single-token system
        cleaned_tokens_info = [
            token_record for token_record in tokens_info
            if token_record["user_id"] != matched_user["user_id"]
        ]

        cleaned_tokens_info.append({
            "user_id": matched_user["user_id"],
            "token": generated_token,
            "created_at": datetime.now().isoformat()
        })
        generic_utils.save_json(settings.TOKEN_FILE, cleaned_tokens_info)

        return json.dumps({
            "token": generated_token,
            "user_id": matched_user["user_id"],
            "is_admin": matched_user["is_admin"]
        })
