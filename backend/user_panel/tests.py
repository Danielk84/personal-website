import uuid
from time import sleep
from datetime import datetime, timezone, timedelta

import jwt
from django.test import TestCase
from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status, exceptions
from rest_framework.test import APIClient

from .auth import (
    generate_token,
    check_token, 
    JWTAuthentication,
    OnlyAdminJWTAuthetication,
)
from .serializers import (
    create_activation_serializer,
    create_full_serializer,
)
from posts.models import Post
from medias.models import Photo


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
        sleep(2)
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

    def test_jwt_authenticate(self):
        token = generate_token(self.user)

        req = HttpRequest()
        req.META['HTTP_AUTHORIZATION'] = f'Token {token}'

        jwt_auth = JWTAuthentication()
        result = jwt_auth.authenticate(req)

        self.assertEqual(result[0], self.user)
        self.assertEqual(token, result[1])

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
        req.META['HTTP_AUTHORIZATION'] = f'Token {token}'
        with self.assertRaisesMessage(exceptions.NotAuthenticated, "Invalid Token."):
            jwt_auth.authenticate(req)


class OnlyAdminJWTAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = "/user-panel/login/"

        self.password = "testpassword"
        self.superuser = User.objects.create_superuser(
            username="testsuperuser",
            password=self.password,
        )
        self.not_superuser = User.objects.create_user(
            username="testnotsuperuser",
            password=self.password,
        )

    def test_superuser_auth(self):
        resp = self.client.post(
            self.login_url,
            data={
                "username": self.superuser.username,
                "password": self.password,
            }
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        req = HttpRequest()
        req.META['HTTP_AUTHORIZATION'] = f'Token {resp.data["Token"]}'

        sleep(1)
        jwt_auth = OnlyAdminJWTAuthetication()
        result = jwt_auth.authenticate(req)

        self.assertEqual(result[0], self.superuser)
        self.assertEqual(result[1], resp.data["Token"])

    def test_not_superuser_auth(self):
        resp = self.client.post(
            self.login_url,
            data={
                "username": self.not_superuser.username,
                "password": self.password,
            }
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        req = HttpRequest()
        req.META['HTTP_AUTHORIZATION'] = f'Token {resp.data["Token"]}'

        sleep(1)
        jwt_auth = OnlyAdminJWTAuthetication()

        with self.assertRaisesMessage(exceptions.PermissionDenied, "Invalid User."):
            jwt_auth.authenticate(req)


class AdminManagerMixinTestCase:
    def test_list(self):
        resp = self.client.get(self.base_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resp.data["results"],
            self.list_serializer(
                self.model.objects.order_by("is_active"), many=True,
            ).data,
        )

    def test_update(self):
        serializer = self.list_serializer(data={"is_active": True})
        serializer.is_valid()

        resp = self.client.put(
            self.base_url + f"{self.obj.slug}/",
            data=serializer.validated_data
        )
        self.obj.refresh_from_db()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, self.list_serializer(self.obj).data)

    def test_retrieve(self):
        resp = self.client.get(self.base_url + f"{self.obj.slug}/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, self.full_serializer(self.obj).data)


class PostActivationViewSetTestCase(AdminManagerMixinTestCase, TestCase):
    def setUp(self):
        self.client = APIClient()

        self.password = "testPassword"
        self.user = User.objects.create_superuser(
            username="testUsername",
            password=self.password,
        )

        self.model = Post

        self.obj = self.model.objects.create(
            title="testTitle",
            user=self.user,
            body="testBody",
            summary="testSummary",
        )

        self.token = "Token " + self.client.post(
            "/user-panel/login/",
            data={
                "username": self.user.username,
                "password": self.password,
            }
        ).data["Token"]
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        self.base_url = "/user-panel/post-activation/"

        self.list_serializer = create_activation_serializer(self.model)
        self.full_serializer = create_full_serializer(self.model)
        sleep(1)


class PhotoActivationViewSetTestCase(AdminManagerMixinTestCase, TestCase):
    def setUp(self):
        self.client = APIClient()

        self.password = "testPassword"
        self.user = User.objects.create_superuser(
            username="testUsername",
            password=self.password,
        )
        self.post = Post.objects.create(
            title="testTitle",
            user=self.user,
            body="testBody",
            summary="testSummary",
        )

        self.model = Photo

        self.obj = self.model.objects.create(
            title="Template",
            post=self.post,
            img=SimpleUploadedFile(
                name=f"{str(uuid.uuid4())}.jpg",
                content=b"file_content",
                content_type="image/jpeg"
            ),
            is_active=False,
        )

        self.token = "Token " + self.client.post(
            "/user-panel/login/",
            data={
                "username": self.user.username,
                "password": self.password,
            }
        ).data["Token"]
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        self.base_url = "/user-panel/photo-activation/"

        self.list_serializer = create_activation_serializer(self.model)
        self.full_serializer = create_full_serializer(self.model)
        sleep(1)