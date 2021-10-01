from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Work(models.Model):
    id = models.IntegerField(primary_key=True)
    key = models.CharField(max_length =255)
    Issue_Type = models.CharField(max_length =255)
    Summary = models.CharField(max_length =255)
    Status = models.CharField(max_length =255)
    Application = models.CharField(max_length =255)


#Otp Model
class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete =models.CASCADE)
    time_st = models.DateTimeField(auto_now = True)
    otp = models.SmallIntegerField()
