from django.db import models
from django.core.signing import TimestampSigner
from django.forms import PasswordInput
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agent = models.TextField(null=True, blank=True)




class File(models.Model):
    file = models.FileField(upload_to='files')
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    security = TimestampSigner(sep="+", salt="files/File")
    password = models.CharField(max_length=50, null=True, blank=True)
    no_of_correct_attempts = models.IntegerField(default=0, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        signed_pk = self.security.sign(self.pk)
        print(signed_pk)
        return reverse("secure-file", kwargs={"signed_pk": signed_pk})
    

class Link(models.Model):
    link = models.TextField()
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    security = TimestampSigner(sep="+", salt="files/Link")
    password = models.CharField(max_length=50, null=True, blank=True)
    no_of_correct_attempts = models.IntegerField(default=0, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        signed_pk = self.security.sign(self.pk)
        return reverse("secure-link", kwargs={"signed_pk": signed_pk})
    