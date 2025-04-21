import os
import uuid
import tempfile
from time import sleep

from PIL import Image
from django.test import TestCase
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Post
from .models import Photo
from .serializers import PhotoSerializer


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


class PhotoManagerViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.password = "testPassword"
        self.user = User.objects.create_user(
            username="testUsername",
            password=self.password,
        )
        self.post = Post.objects.create(
            title="testTitle",
            user=self.user,
            body="testBody",
            summary="testSummary",
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
            is_active=True,
        )
        self.file_path = self.photo.img.path

        self.token = "Token " + self.client.post(
            "/user-panel/login/",
            data={
                "username": self.user.username,
                "password": self.password,
            }
        ).data["Token"]
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.base_url = "/medias/photos/"
        sleep(1)

    def test_retrieve(self):
        resp = self.client.get(
            self.base_url + f"{self.photo.slug}/?post={self.post.slug}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, PhotoSerializer(self.photo).data)

    def test_list(self):
        resp = self.client.get(
            self.base_url + f"?post={self.post.slug}",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resp.data,
            PhotoSerializer(Photo.objects.filter(post=self.post), many=True).data,
        )

    def test_destroy(self):
        slug = self.photo.slug
        resp = self.client.delete(
            self.base_url + f"{self.photo.slug}/?post={self.post.slug}"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Photo.objects.filter(slug=slug).count(), 0)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


class UploadPhotoAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.password = "testPassword"
        self.user = User.objects.create_user(
            username="testUsername",
            password=self.password,
        )
        self.post = Post.objects.create(
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
        self.base_url = "/medias/upload-photo/"

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
        sleep(1)

    def test_create(self):
        title = "test_title"
        img = Image.new('RGB', (500, 500), color='white')

        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_f:
            img.save(temp_f, format="JPEG")
            temp_f.seek(0)
            
            resp = self.client.post(
                self.base_url + f"?post={self.post.slug}",
                data = {
                    "title": title,
                    "img": SimpleUploadedFile(
                        name=temp_f.name,
                        content=temp_f.read(),
                        content_type="image/jpeg"
                    ),
                },
                format="multipart",
            )

            self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
            photo = Photo.objects.get(title=title)

            temp_f.seek(0)
            with open(photo.img.path, "rb+") as f:
                self.assertEqual(f.read(), temp_f.read())

    def test_update(self):
        img = Image.new('RGB', (500, 500), color='white')

        photo = Photo.objects.get(title=self.photo.title)

        with tempfile.NamedTemporaryFile(prefix="new_", suffix=".jpg") as temp_f:
            img.save(temp_f, format="JPEG")
            temp_f.seek(0)

            resp = self.client.put(
                self.base_url + photo.slug + f"/?post={self.post.slug}",
                data = {
                    "title": self.photo.title,
                    "img": SimpleUploadedFile(
                        name=temp_f.name,
                        content=temp_f.read(),
                        content_type="image/jpeg"
                    ),
                },
                format="multipart",
            )

            self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
            photo = Photo.objects.get(title=self.photo.title)

            temp_f.seek(0)
            with open(photo.img.path, "rb+") as f:
                self.assertEqual(f.read(), temp_f.read())

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


class ServerPhotoViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.password = "testPassword"
        self.user = User.objects.create_user(
            username="testUsername",
            password=self.password,
        )
        self.post = Post.objects.create(
            title="testTitle",
            user=self.user,
            body="testBody",
            summary="testSummary",
        )

        self.active_photo = Photo.objects.create(
            title="Template",
            post=self.post,
            img=SimpleUploadedFile(
                name=f"{str(uuid.uuid4())}.jpg",
                content=b"file_content",
                content_type="image/jpeg"
            ),
            is_active=True,
        )
        self.inactive_photo = Photo.objects.create(
            title="NOTTemplate",
            post=self.post,
            img=SimpleUploadedFile(
                name=f"{str(uuid.uuid4())}.jpg",
                content=b"file_content",
                content_type="image/jpeg"
            ),
            is_active=False,
        )
        self.base_url = "/md_files/"

    def test_active_photo(self):
        resp = self.client.get(self.base_url + str(self.active_photo.img))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_inactive_photo(self):
        resp = self.client.get(self.base_url + str(self.inactive_photo.img))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        os.remove(self.active_photo.img.path)
        os.remove(self.inactive_photo.img.path)