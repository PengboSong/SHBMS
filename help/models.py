from django.db import models


class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
