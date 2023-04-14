# Create your models here.
from django.db import models


# Create your models here.

class pet(models.Model):
    pet_type = models.CharField(max_length=30)
    pet_breed = models.CharField(max_length=30)
    pet_location = models.CharField(max_length=30)

    pet_bloodline = models.CharField(max_length=30)

    pet_nos = models.DecimalField(decimal_places=0, max_digits=2)
    pet_rem = models.DecimalField(decimal_places=0, max_digits=2)
    pet_price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.pet_type


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    PET_STATUSES = ((BOOKED, 'Booked'),
                    (CANCELLED, 'Cancelled'),)
    email = models.EmailField()

    name = models.CharField(max_length=30)

    userid = models.DecimalField(decimal_places=0, max_digits=2)

    pet_id = models.DecimalField(decimal_places=0, max_digits=2)

    pet_type = models.CharField(max_length=30, default='Dog')
    pet_breed = models.CharField(max_length=30)
    pet_location = models.CharField(max_length=30)
    pet_bloodline = models.CharField(max_length=30)

    pet_nos = models.DecimalField(decimal_places=0, max_digits=2)
    pet_price = models.DecimalField(decimal_places=2, max_digits=6)

    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=PET_STATUSES, default=BOOKED, max_length=2)

    def __str__(self):
        return self.email
