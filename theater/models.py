from django.db import models

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

    