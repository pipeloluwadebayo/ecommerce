from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=250)
    address_line_2 = models.CharField(max_length=250)
    state = models.CharField(max_length=100)
    country = CountryField()




