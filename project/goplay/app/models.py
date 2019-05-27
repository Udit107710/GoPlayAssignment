from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class Post(models.Model):
    file = models.ImageField(upload_to="uploads/")
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE,
            )

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    text = models.TextField()

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete= models.CASCADE)
    reply = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
