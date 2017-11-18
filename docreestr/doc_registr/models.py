from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class UserDoc(AbstractBaseUser):
    name = models.CharField(max_length = 50, unique = True)
    INN = models.TextField()
    wallet = models.TextField()
    walletKey = models.TextField()
    USERNAME_FIELDS = 'name'
    REQUIRED_FIELDS = ['INN']

    def create_user(self, name, INN, password=None):

class Status(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()

class Document(models.Model):
    name = models.CharField(max_length= 50)
    id_status = models.ForeignKey(Status)
    id_user = models.ForeignKey(User)
    hash_file = models.TextField()
