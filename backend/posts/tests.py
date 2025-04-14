from datetime import timedelta

import orjson
from django.test import TestCase
from django.utils import timezone
from django.core.cache import cache
from django.template.defaultfilters import slugify
from rest_framework import status
from rest_framework.test import APIClient

from .models import Post
from .serializers import (
    PostSerializer,
    PostOverviewSerializer,
)


class PostModelTestCase(TestCase):
    def setUp(self):
        for i in range(5):
            Post.objects.create(
                title=f"title: {i}",
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
        self.active_post =  Post.objects.create(
                title="title: 1", is_active=True,
                body="body 1", summary="summary 1",
            )
        self.inactive_post =  Post.objects.create(
                title="title: 2", is_active=False,
                body="body 2", summary="summary 2",
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
        for i in range(30):
            Post.objects.create(
                title=f"title: {i}",
                is_active=True if i & 1 else False,
                body=f"body {i}",
                summary=f"summary {i}",
                pub_date = timezone.now() - timedelta(days=1)
            )

    def test_overview(self):
        resp = self.client.get(self.base_url + "/overview/")
        serialized_data = PostOverviewSerializer(
            Post.objects.published()[:4],
            many=True,
        ).data

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serialized_data)

    def test_list(self):
        resp = self.client.get(self.base_url + "/")
        serialized_data = PostOverviewSerializer(
            Post.objects.published()[:10],
            many=True,
        ).data
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["results"], serialized_data)

        resp = self.client.get(self.base_url + "/?page=2")
        serialized_data = PostOverviewSerializer(
            Post.objects.published()[10:20],
            many=True,
        ).data
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["results"], serialized_data)