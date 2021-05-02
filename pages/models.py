from django.db import models
from datetime import datetime

# Model for Bank details

class Bank(models.Model):

    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)

    def __str__(self):
        return self.name

class Details(models.Model):

    name = models.CharField(max_length=200)
    interest = models.CharField(max_length=200)
    fees = models.CharField(max_length=200)

    def __str__(self):
        return self.name