from django.db import models
import datetime

now = datetime.datetime.now()

class messbrd(models.Model):
    MID = models.CharField('使用者編號', max_length=100 )
    MCont = models.CharField('內容', max_length=1000 )
    MDATE = models.DateTimeField() 