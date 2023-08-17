from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing

def product(request, id):
    productDetails = Listing.objects.get(pk=id)
    onWatchList = request.user in productDetails.toWatchList.all()
    return render(request,"auctions/product.html", {
        "product": productDetails,
        "onWatchList": onWatchList
    })

def toWatchList(request):
    theCurrentUser = request.user
    lists = theCurrentUser.WatchListForUsers.all()
    return render(request, "auctions/toWatchList.html", {
        "lists": lists
    })

def removeFromWatchList(request,id):
    productDetails = Listing.objects.get(pk=id)
    theCurrentUser = request.user
    productDetails.toWatchList.remove(theCurrentUser)
    return HttpResponseRedirect(reverse("product", args=[id]))


def addToWatchList(request,id):
    productDetails = Listing.objects.get(pk=id)
    theCurrentUser = request.user
    productDetails.toWatchList.add(theCurrentUser)
    return HttpResponseRedirect(reverse("product", args=[id]))

def index(request):
    activeList = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeList,
        "categories": categories
    })

def viewCategory(request):
    if request.method == "POST":
        categoryForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryForm)
        activeList = Listing.objects.filter(isActive=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeList,
            "categories": categories
    })

def createListing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imgUrl = request.POST["imgUrl"]
        price = request.POST["price"]
        category = request.POST["category"]

        thecurrentUser = request.user

        categoryInf = Category.objects.get(categoryName = category)
        
        newListing= Listing(
            title = title,
            description = description,
            imgUrl = imgUrl,
            price = float(price),
            category = categoryInf,
            owner = thecurrentUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
