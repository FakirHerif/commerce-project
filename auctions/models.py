from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return self.categoryName


class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidUser")

    def ___str___(self):
        return self.bid

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=640)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category" )
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    imgUrl = models.CharField(max_length=6400)
    isActive = models.BooleanField(default=True)
    toWatchList = models.ManyToManyField(User, blank=True, null=True, related_name="WatchListForUsers")

    def __str__(self):
        return self.title

class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userMsg")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="productMsg")
    msg = models.CharField(max_length=640)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.writer} comment on {self.listing}"
    
