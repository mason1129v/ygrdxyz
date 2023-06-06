from django.db import models
import datetime

now = datetime.datetime.now()

class messbrd(models.Model):
    MID = models.CharField('使用者編號', max_length=100 )
    MCont = models.CharField('內容', max_length=1000 )
    MDATE = models.DateTimeField() 

class member(models.Model):
    MID = models.AutoField('會員編號', primary_key=True)
    MPW = models.CharField('會員密碼', max_length=20, null=False)
    MAC = models.CharField('會員帳號', max_length=50, null=False)

class product(models.Model):
    PID = models.CharField('產品', max_length=10 )
    PName = models.CharField('產品名稱', max_length=20, null=False)
    PDetail = models.CharField('產品內容', max_length=100, null=False)