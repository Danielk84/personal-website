import uuid

from django.db import models
from django.template.defaultfilters import slugify

from posts.models import Post


class Photo(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(allow_unicode=True, unique=True)
    is_active = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="photos/%Y/%m/%d")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        _UUID = str(uuid.uuid4())
        self.slug = slugify(f"{self.name}-{_UUID}")
        return super().save(*args, **kwargs)

    def is_published(self) -> bool:
        return self.is_active