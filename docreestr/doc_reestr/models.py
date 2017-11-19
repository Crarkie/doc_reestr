from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 50, unique= True)
    INN = models.TextField(unique = True)
    password = models.TextField()
    file = models.FileField()

class Status(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()

class Document(models.Model):
    name = models.CharField(max_length= 50)
    id_status = models.ForeignKey(Status)
    id_user = models.ForeignKey(User)
    hash_file = models.TextField()
