import orjson
from django.test import TestCase
from django.core.cache import cache
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from .models import Post
from .serializers import (
    PostManagerSerializer,
    PostOverviewSerializer,
)


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testUser",
            password="testPassword",
        )
        for i in range(5):
            Post.objects.create(
                title=f"title: {i}",
                user=self.user,
                is_active=True if i & 1 else False,
                body=f"body {i}",
                summary=f"summary {i}",
            )

    def test_active_queryset(self):
        posts = Post.objects.active()
        self.assertEqual(posts.count(), 2)

    def test_published_queryset(self):
        posts = Post.objects.published()
        self.assertEqual(posts.count(), 2)

    def test_slug_value(self):
        post = Post.objects.first()
        self.assertEqual(post.title, "title: 4")

        self.assertEqual(
            post.slug,
            slugify(f"{post.title}-{post.pub_date}"),
        )

    def test_save_method(self):
        post = Post.objects.last()
        self.assertEqual(post.title, "title: 0")

        post.title = "changing post title"
        last_modify = post.last_modify
        post.save()
        self.assertNotEqual(post.last_modify, last_modify)


class PostViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = "/post/"
        self.user = get_user_model().objects.create_user(
            username="testUser",
            password="testPassword",
        )
        self.active_post =  Post.objects.create(
                title="title: 1", is_active=True,
                body="body 1", summary="summary 1",
                user=self.user,
            )
        self.inactive_post =  Post.objects.create(
                title="title: 2", is_active=False,
                body="body 2", summary="summary 2",
                user=self.user,
            )

    def test_get_post(self):
        resp = self.client.get(self.base_url + self.active_post.slug + "/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resp.data,
            orjson.loads(cache.get(f"post-{self.active_post.slug}"))
        )

        resp = self.client.get(self.base_url + self.inactive_post.slug + "/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class PostListViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = "/posts"

        self.user = get_user_model().objects.create_user(
            username="testUser",
            password="testPassword",
        )
        for i in range(30):
            Post.objects.create(
                title=f"title: {i}",
                is_active=True if i & 1 else False,
                body=f"body {i}",
                summary=f"summary {i}",
                pub_date = '2025-04-17 09:03:53.228014+00:00',
                user=self.user,
            )

    def test_overview(self):
        resp = self.client.get(self.base_url + "/overview/")
        serialized_data = PostOverviewSerializer(
            Post.objects.published()[:4],
            many=True,
        ).data

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serialized_data)
        self.assertEqual(resp.data, orjson.loads(cache.get("post-overview")))

    def test_list(self):
        resp = self.client.get(self.base_url + "/")
        serialized_data = PostOverviewSerializer(
            Post.objects.published()[:10],
            many=True,
        ).data
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["results"], serialized_data)
        self.assertEqual(resp.data, orjson.loads(cache.get("post-list-page-1")))

        resp = self.client.get(self.base_url + "/?page=2")
        serialized_data = PostOverviewSerializer(
            Post.objects.published()[10:20],
            many=True,
        ).data
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["results"], serialized_data)
        self.assertEqual(resp.data, orjson.loads(cache.get("post-list-page-2")))

class PostManagerViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.baseurl = "/post-mng/"

        self.username = "testUser"
        self.password = "testPassword"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.post = Post.objects.create(
            title="basetitle",
            user=self.user,
            body="body",
            summary="summary",
        )
        self.token = "Token " + self.client.post(
            "/user-panel/login/",
            data={
                "username": self.username,
                "password": self.password,
            }
        ).data["Token"]
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_create(self):
        data = {
            "title": "This is a valid title",
            "body": "This is the content of the post.",
            "summary": "This is the summary.",
        }
        resp = self.client.post(self.baseurl, data, format="json")

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            resp.data,
            PostManagerSerializer(
                Post.objects.filter(**data).first(),
            ).data,
        )

    def test_update(self):
        data = {
            "title": "This is a older valid title",
            "user": self.user,
            "body": "This is the older content of the post.",
            "summary": "This is the older summary.",
            "is_active": True,
        }
        post = Post.objects.create(**data)

        data = {
            "title": "This is a new valid title",
            "body": "This is the new content of the post.",
            "summary": "This is the new summary.",
        }
        resp = self.client.put(
            self.baseurl + f"{post.slug}/", data, format="json"
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(resp.data, PostManagerSerializer(post).data)

    def test_list(self):
        user2 = get_user_model().objects.create_user(
            username="user2",
            password="password2",
        )
        for i in range(40):
            Post.objects.create(
                title=f"title-{i}",
                user=self.user if i & 1 else user2,
                body="some body",
                summary="some summary",
            )
        resp = self.client.get(self.baseurl + "?page=1")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data["results"], PostManagerSerializer(
                Post.objects.filter(user=self.user)[:10],
                many=True,
            ).data
        )

    def test_retrieve(self):
        resp = self.client.get(self.baseurl + f"{self.post.slug}/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, PostManagerSerializer(self.post).data)

    def test_auth(self):
        client = APIClient()

        resp = client.get(self.baseurl)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy(self):
        resp = self.client.delete(self.baseurl + f"{self.post.slug}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)