import uuid
from datetime import datetime, timezone, timedelta

import jwt
import orjson
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from backend.celery import set_cache


def generate_token(user) -> str | None:
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


def check_token(token: str):
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
        user = get_user_model().objects.get(
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
    except Exception:
        return None


class JWTAuthentication(TokenAuthentication):
    """
    Custom authentication class for validating JSON Web Tokens (JWTs).

    This class extends DRF's TokenAuthentication and overrides the 
    `authenticate_credentials` method to validate and authenticate a user
    based on the provided JWT.

    Features:
    1. Validates the given JWT using a custom `check_token` function.
    2. Retrieves the authenticated user associated with the valid token.
    3. Raises an exception if the token is invalid, expired, or fails validation.

    """
    def authenticate_credentials(self, key):
        """
        This method used by authentication method in TokenAuthentication,
        so it not used directly.
        """
        if not (user := check_token(key)):
            raise exceptions.NotAuthenticated("Invalid Token.")

        return (user, key)


class OnlyAdminJWTAuthetication(TokenAuthentication):
    """
    Custom JWT authentication class that allows access only to superusers.

    This class extends DRF's TokenAuthentication and overrides the 
    `authenticate_credentials` method to validate and authenticate a user
    based on the provided JWT.

    This authentication method verifies the provided JWT token, ensuring that:
    1. The token is valid and corresponds to an authenticated user.
    2. The authenticated user has superuser privileges (`is_superuser=True`).
    3. If either condition is not met, appropriate exceptions are raised.
    """
    def authenticate_credentials(self, key):
        """
        This method used by authentication method in TokenAuthentication,
        so it not used directly.
        """
        if not (user := check_token(key)):
            raise exceptions.NotAuthenticated("Invalid Token.")

        if not user.is_superuser:
            raise exceptions.PermissionDenied("Invalid User.")

        return (user, key)