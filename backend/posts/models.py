from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class PostQuerySet(models.QuerySet):
    """
    Custom QuerySet for filtering published and active posts.

    This QuerySet provides convenient methods for retrieving posts
    based on their publication status and activity.
    """

    def published(self) -> models.QuerySet:
        """
        Returns only published posts.

        A post is considered published if:
        - It is active.
        - Its `pub_date` is in the past (before or equal to the current time).

        Returns:
            QuerySet: A queryset containing published posts.
        """
        return self.active().filter(pub_date__lte=timezone.now())

    def active(self) -> models.QuerySet:
        """
        Returns only active posts.

        A post is considered active if its `is_active` field is set to `True`.

        Returns:
            QuerySet: A queryset containing active posts.
        """
        return self.filter(is_active=True)


class Post(models.Model):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(allow_unicode=True, unique=True)
    is_active = models.BooleanField(default=False)
    body = models.TextField()
    summary = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    last_modify = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-pub_date"]
        indexes = [
            models.Index(fields=["title", "is_active", "pub_date", "last_modify"])
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title}-{self.pub_date}")
        super().save(*args, **kwargs)

    def is_published(self) -> bool:
        return self.is_active and self.pub_date < timezone.now()