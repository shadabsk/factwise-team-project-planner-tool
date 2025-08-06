import os
import json
import hashlib
import uuid
from datetime import datetime

from django.conf import settings


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(user_id):
    seed = user_id + str(uuid.uuid4()) + datetime.now().isoformat()
    return hashlib.sha256(seed.encode()).hexdigest()


def get_user_from_token(current_token):
    if not os.path.exists(settings.TOKEN_FILE):
        return None
    with open(settings.TOKEN_FILE) as t_file:
        tokens_info = json.load(t_file)
    token_entry = next(
        (
            token_record for token_record in tokens_info
            if token_record["token"] == current_token
        ),
        None
    )
    if not token_entry:
        return None
    with open(settings.USER_FILE) as u_file:
        users_info = json.load(u_file)
    return next(
        (
            user_record for user_record in users_info
            if user_record["user_id"] == token_entry["user_id"]
        ),
        None
    )
