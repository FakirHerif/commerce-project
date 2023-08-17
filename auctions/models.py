from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return self.categoryName

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=640)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category" )
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    imgUrl = models.CharField(max_length=6400)
    isActive = models.BooleanField(default=True)
    toWatchList = models.ManyToManyField(User, blank=True, null=True, related_name="WatchListForUsers")

    def __str__(self):
        return self.title

