import uuid
from datetime import datetime, timezone, timedelta

import jwt
import orjson
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache

from backend.celery import set_cache


def generate_token(user: User) -> str | None:
    """
    Generates a JSON Web Token (JWT) for a given user and stores it in the cache.

    This function performs the following steps:
    1. Creates a cache key using the user's ID and username.
    2. Checks if a valid token already exists in the cache. If yes, it returns the cached token.
    3. Generates a unique UUID and encodes a JWT with user-specific data and expiration.
    4. Asynchronously stores the token and UUID in the cache using a Celery task.
    """
    try:
        key = f"{user.id}-{user.username}"

        if value := cache.get(key):
            token = orjson.loads(value)["token"]
        else:
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
            set_cache.delay(key, orjson.dumps({"UUID": _UUID, "token": token}))

        return token
    except Exception as e:
        raise e


def check_token(token: str) -> User | None:
    """
    Validates a JWT token and retrieves the associated user if the token is valid.

    This function performs the following steps:
    1. Decodes the JWT token using the secret key and algorithm specified in settings.
    2. Retrieves the user from the database using the `user_id` and `username` from the payload.
    3. Fetches the cached data associated with the user's token from the cache.
    4. Validates the UUID and token against the cached data to ensure consistency.
    """
    try:
        payload = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM,]
        )
        user = User.objects.get(
            pk=payload["user_id"],
            username=payload["username"],
        )
        cache_data = orjson.loads(cache.get(f"{user.id}-{user.username}"))

        assert (
            cache_data and
            cache_data["UUID"] == payload["UUID"] and
            cache_data["token"] == token
        )
        return user
    except Exception as e:
        return None