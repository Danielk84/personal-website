from django.test import TestCase
from django.template.defaultfilters import slugify

from .models import Post


class PostTestCase(TestCase):
    def setUp(self):
        for i in range(5):
            Post.objects.create(
                title=f"title: {i}",
                is_active=True if (i & 1) == 0 else False,
                body=f"body {i}",
                summary=f"summary {i}",
            )

    def test_active_queryset(self):
        posts = Post.objects.active()
        self.assertEqual(posts.count(), 3)

    def test_published_queryset(self):
        posts = Post.objects.published()
        self.assertEqual(posts.count(), 3)

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