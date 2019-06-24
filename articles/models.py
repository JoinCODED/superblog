from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=125)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    created = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField(default=False)
    published = models.DateTimeField(null=True)
    slug = models.SlugField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
