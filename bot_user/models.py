from django.db import models

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)

    photo = models.ImageField(upload_to='media/', null=True, blank=True)
    video = models.FileField(upload_to='media/videos', null=True, blank=True)
    voice = models.FileField(upload_to='media/audios', null=True, blank=True)
    document = models.FileField(upload_to='media/files', null=True, blank=True)

    location = models.JSONField(null=True)
    contact = models.CharField(max_length=16)


    def __str__(self):
        return f'{self.name} {self.surname} id={self.user_id}'

class Tguser(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)

    photo = models.CharField(max_length=128)
    video = models.CharField(max_length=128)
    voice = models.CharField(max_length=128)
    document = models.CharField(max_length=128)

    location = models.JSONField(null=True)
    contact = models.CharField(max_length=16)


    def __str__(self):
        return f'{self.name} {self.surname} id={self.user_id}'