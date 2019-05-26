from django.conf import settings
from django.db import models

class Post(models.Model):
    image = models.ImageField(upload_to="uploads/")
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE,
            )

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    text = models.TextField()

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete= models.CASCADE)
    reply = models.TextField(null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
