from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    DESIG = [
        ("Manager", "Manager"),
        ("Desk Clerk", "Desk Clerk"),
        ("IT Support", "IT Support"),
    ]
    designation = models.CharField(max_length = 20, choices = DESIG, default = "User")

    def __str__(self):
        return "{}, {}".format(self.user.username, self.designation)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Create your models here.
class movie(models.Model):
    title = models.CharField(max_length = 30, default = "Unreleased")
    genre = models.CharField(max_length = 20)
    air_till = models.DateField()
    rating = models.FloatField()
    starring = models.TextField(max_length=300)

    def __str__(self):
        return "{}:{}:{}".format(self.title, self.genre, self.rating)

class theatre(models.Model):
    theatre_name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 30)
    city = models.CharField(max_length = 30)
    state = models.CharField(max_length = 30)

    @property
    def location(self):
        return '{}, {}, {}'.format(self.address, self.city, self.state)

    def __str__(self):
        return self.location

class currentlyshowing(models.Model):
    theatre = models.OneToOneField(theatre, on_delete=models.CASCADE)
    movie = models.OneToOneField(movie, on_delete=models.CASCADE)
    time = models.TimeField()
    capacity = models.IntegerField()
    cine_no = models.IntegerField()


    @property
    def cine(self):
        return "{}, {}".format(self.capacity, self.cine_no)

    def __str__(self):
        return self.cine_no
        