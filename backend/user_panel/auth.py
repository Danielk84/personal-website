import uuid
from datetime import datetime, timezone, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import User


def generate_token(user: User) -> str | None:
    try:
        _UUID = str(uuid.uuid4())

        token = jwt.encode(
            payload={
                "user_id": user.id,
                "username": user.username,
                "UUID": _UUID,
                "exp": datetime.now(timezone.utc) +
                    timedelta(minutes=settings.TOKEN_EXPIRED_TIME),
            },
            key=settings.SECRET_KEY,
            algorithm=settings.TOKEN_ALGORITHM,
        )
        return token
    except Exception as e:
        raise e