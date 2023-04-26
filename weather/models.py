from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save


class Location(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.ManyToManyField(Location)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            first_name=user.username,
            email=user.email
        )


post_save.connect(createProfile, User)
