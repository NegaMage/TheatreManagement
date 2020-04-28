from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name = "Date of Birth", null=True, blank=True)
    DESIG = [
        ("Manager", "Manager"),
        ("Desk Clerk", "Desk Clerk"),
        ("IT Support", "IT Support"),
    ]
    designation = models.CharField(verbose_name = "Designation", max_length = 20, choices = DESIG, default = "User")

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
class Movie(models.Model):
    title = models.CharField(verbose_name = "Title", max_length = 30, default = "Unreleased")
    genre = models.CharField(verbose_name = "Genre", max_length = 20)
    air_till = models.DateField(verbose_name = "Showing till")
    rating = models.FloatField(verbose_name = "Rating")
    starring = models.TextField(verbose_name = "Starring", max_length=300)
    poster = models.ImageField(verbose_name="Poster",upload_to="poster",blank=True)

    def clean(self):
        if self.rating > 5 or self.rating < 0 :
            raise ValidationError(gettext_lazy('Rating is on 5 point scale'))
        

    def __str__(self):
        return "{}:{}:{}".format(self.title, self.genre, self.rating)

class Theatre(models.Model):
    theatre_name = models.CharField(verbose_name = "Theatre", max_length = 30)
    address = models.CharField(verbose_name = "Address", max_length = 30)
    capacity = models.IntegerField(verbose_name="Max Seating")
    city = models.CharField(verbose_name = "City", max_length = 30)
    state = models.CharField(verbose_name = "State", max_length = 30)

    def __str__(self):
        return '{}, {}, {}'.format(self.address, self.city, self.state)

class Show(models.Model):
    theatre = models.OneToOneField(Theatre, on_delete=models.CASCADE)
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    time = models.TimeField(verbose_name = "Duration")
    capacity = models.IntegerField(verbose_name = "Seats left")
    cine_no = models.IntegerField(verbose_name = "Cinema Number")

    

    @property
    def cine(self):
        return "{}, {}".format(self.capacity, self.cine_no)

    def __str__(self):
        return "{}".format(self.cine_no)
        
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats = models.IntegerField(default=1)
