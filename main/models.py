import datetime
from django.db import models
from django.utils import timezone

# Create models

class Message(models.Model):
    msg_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.msg_text
    def recently_published(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Response(models.Model):
    question = models.ForeignKey(Message, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('data published')

    def __str__(self):
        return self.response_text
    def recently_published(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
