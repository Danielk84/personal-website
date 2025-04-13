import uuid
from datetime import datetime, timezone, timedelta

import jwt
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .auth import generate_token, check_token


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_generate_token(self):
        token = generate_token(self.user)

        self.assertIsNotNone(token)
        self.assertEqual(token, generate_token(self.user))

    def test_check_token(self):
        token = generate_token(self.user)

        self.assertEqual(check_token(token), self.user)

        _UUID = str(uuid.uuid4())
        token = jwt.encode(
            payload={
                "user_id": self.user.id,
                "username": self.user.username,
                "UUID": _UUID,
                "exp": datetime.now(timezone.utc) +
                    timedelta(minutes=settings.TOKEN_EXPIRED_TIME),
            },
            key=settings.SECRET_KEY,
            algorithm=settings.TOKEN_ALGORITHM,
        )
        self.assertIsNone(check_token(token))

    def test_jwt_login_view(self):
        resp = self.client.post(
            "/user-panel/login/",
            data={
                "username": self.username,
                "password": self.password,
            }
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        user = check_token(resp.data["Token"])
        self.assertEqual(user, self.user)