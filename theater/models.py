from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.utils.text import slugify
from django.utils import timezone 

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
    slug_title = models.SlugField(verbose_name="Url Slug", max_length=30)
    genre = models.CharField(verbose_name = "Genre", max_length = 20)
    air_till = models.DateField(verbose_name = "Showing till")
    rating = models.FloatField(verbose_name = "Rating")
    starring = models.TextField(verbose_name = "Starring", max_length=300)
    poster = models.ImageField(verbose_name="Poster",upload_to="poster",blank=True)
    blurb = models.TextField(verbose_name="Summary", max_length=300)
    show = models.ManyToManyField('Theatre', through='Show', related_name='showing_at')
    def clean(self):
        if self.rating > 5 or self.rating < 0 :
            raise ValidationError(gettext_lazy('Rating is on 5 point scale'))
        

    def __str__(self):
        return "{}:{}:{}".format(self.title, self.genre, self.rating)

class Theatre(models.Model):
    theatre_name = models.CharField(verbose_name = "Theatre", max_length = 30)
    slug_name = models.SlugField(verbose_name="Url Slug", max_length=30)
    address = models.CharField(verbose_name = "Address", max_length = 30)
    capacity = models.IntegerField(verbose_name="Max Seating")
    city = models.CharField(verbose_name = "City", max_length = 30)
    state = models.CharField(verbose_name = "State", max_length = 30)
    showing = models.ManyToManyField('Movie', through='Show', related_name='now_showing')
    def __str__(self):
        return '{}, {}, {}, {}'.format(self.theatre_name, self.address, self.city, self.state)



class Show(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='now_showing')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showing_at')
    cine_no = models.CharField(max_length=5, verbose_name = "Cinema Hall")


    def __str__(self):
        return "{}-{}".format(self.theatre.theatre_name, self.movie.title)
    
    def save(self, *args, **kwargs): 
        super(Show, self).save(*args, **kwargs)
        timelist = ['1100', '1400', '1700', '2000']
        # objlist = []
        for time in timelist:
            timeobj = Times()
            timeobj.time = time
            timeobj.capacity = self.theatre.capacity
            timeobj.show = self
            super(Times, timeobj).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['theatre', 'movie'], name="Only one show for a pair of theatre and movie")
        ]

class Times(models.Model):
    times = [
        ('1100','1100'),
        ('1400','1400'),
        ('1700','1700'),
        ('2000','2000'),
    ]
    time = models.CharField(verbose_name = "Screening time", choices=times, max_length=10)
    show = models.ForeignKey(to='Show', on_delete=models.CASCADE)
    capacity = models.IntegerField(verbose_name = "Seats left",default=9999)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['time', 'show'], name="Unique timing for show")
        ]

    def __str__(self):
        return "{} at {}:{}, {} seats left".format(self.show.movie.title, self.show.theatre.theatre_name, self.time, self.capacity)

    def save(self, *args, **kwargs): 
        if self.capacity > self.show.theatre.capacity :
            self.capacity = self.show.theatre.capacity
        super(Times, self).save(*args, **kwargs)
        


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    time = models.ForeignKey(to=Times, on_delete=models.CASCADE, null=True)
    seats = models.IntegerField(default=1)
    date = models.DateField(verbose_name="Date")

    def clean(self):
        if self.date > self.time.show.movie.air_till :
            raise ValidationError(gettext_lazy('We won\'t be airing that movie then.'))
        today = timezone.now().today().date()
        if self.date < today :
            raise ValidationError(gettext_lazy('You can\'t book before today'))

    def save(self, *args, **kwargs): 
        self.time.capacity -= self.seats
        super(Times, self.time).save(*args, **kwargs)
        super(Transaction, self).save(*args, **kwargs) 

