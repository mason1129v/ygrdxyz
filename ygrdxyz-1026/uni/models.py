from django.db import models
import datetime

now = datetime.datetime.now()

class messbrd(models.Model):
    MID = models.CharField('使用者編號', max_length=100 )
    MCont = models.CharField('內容', max_length=1000 )
    MDATE = models.DateTimeField() 

class c_messbrd(models.Model):
    MID = models.CharField('使用者編號', max_length=100 )
    MCont = models.CharField('內容', max_length=1000 )
    MDATE = models.DateTimeField()  


class Notifications(models.Model):
    message = models.CharField(max_length=255)
    viewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

