import os
import uuid
from time import sleep

from django.test import TestCase
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post
from .models import Photo


class PhotoModelTestCase(TestCase):
    def setUp(self):
        self.username = "testUser"
        self.password = "testPassword"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.post = Post.objects.create(
            title="title",
            user=self.user,
            body="body",
            summary="summary",
        )
        self.img_name = str(uuid.uuid4())
        self.photo = Photo.objects.create(
            title="Template",
            post=self.post,
            img=SimpleUploadedFile(
                name=f"{self.img_name}.jpg",
                content=b"file_content",
                content_type="image/jpeg"
            ),
        )
        self.file_path = self.photo.img.path

    def test_slug_value(self):
        self.assertTrue(
            self.photo.slug.startswith(slugify(self.photo.title))
        )

        old_slug = self.photo.slug
        self.photo.save()
        self.assertTrue(
            self.photo.slug.startswith(slugify(self.photo.title))
        )
        self.assertNotEqual(old_slug, self.photo.slug)

    def test_img_file(self):
        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, "rb+") as f:
            self.assertEqual(f.read(), self.photo.img.read())

    def test_delete_model(self):
        self.photo.delete()

        sleep(2)
        self.assertFalse(os.path.exists(self.file_path))

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)