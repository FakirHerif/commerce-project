from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import User, Category, Listing, Comment, Bid

def product(request, id):
    productDetails = Listing.objects.get(pk=id)

    if not productDetails.isActive:
        bidding_closed = True
    else:
        bidding_closed = False

    onWatchList = request.user in productDetails.toWatchList.all()
    showComments = Comment.objects.filter(product=productDetails)
    isOwner = request.user.username == productDetails.owner.username

    winning_bid = None
    winner = None
    if not productDetails.isActive:
        if productDetails.price.user == request.user:
            winning_bid = productDetails.price
        else:
            winning_bid = productDetails.price
            winner = productDetails.price.user

    return render(request,"auctions/product.html", {
        "product": productDetails,
        "onWatchList": onWatchList,
        "showComments": showComments,
        "isOwner" : isOwner,
        "bidding_closed": bidding_closed,
        "winning_bid": winning_bid,
        "winner": winner 
    })

def closed_listings(request):
    selected_category = request.GET.get('category')
    closed_list = Listing.objects.filter(isActive=False)

    if selected_category:
        category_obj = Category.objects.get(categoryName=selected_category)
        closed_list = closed_list.filter(category=category_obj)

    categories = Category.objects.all()
    return render(request, "auctions/closed_listings.html", {
        "closed_listings": closed_list,
        "categories": categories,
        "selected_category": selected_category
    })




def disableBid(request, id):
    productDetails = Listing.objects.get(pk=id)
    productDetails.isActive = False
    productDetails.save()
    onWatchList = request.user in productDetails.toWatchList.all()
    showComments = Comment.objects.filter(product=productDetails)
    isOwner = request.user.username == productDetails.owner.username    
    return render(request,"auctions/product.html", {
        "product": productDetails,
        "onWatchList": onWatchList,
        "showComments": showComments,
        "isOwner" : isOwner,
        "update" : True,
        "msg" : "CONGRATULATIONS AUCTION IS OVER"
    })    


def addBid(request, id):
    if request.method == "POST":
        newBid = request.POST.get('newBid', None)
        productDetails = Listing.objects.get(pk=id)
        onWatchList = request.user in productDetails.toWatchList.all()
        showComments = Comment.objects.filter(product=productDetails)
        isOwner = request.user.username == productDetails.owner.username

        if isOwner:
            bidError = "You cannot place a bid on your own product."
        else:
            bidError = None

            if newBid is not None and newBid != '':
                try:
                    newBid = int(newBid)
                    current_highest_bid = productDetails.price.bid if productDetails.price else 0

                    if newBid > current_highest_bid:
                        updateBid = Bid(user=request.user, bid=newBid)
                        updateBid.save()

                        if productDetails.price:
                            productDetails.price.delete()

                        productDetails.price = updateBid
                        productDetails.save()
                        return render(request, "auctions/product.html",{
                            "product": productDetails,
                            "msg": "Bid was updated SUCCESSFULLY",
                            "update": True,
                            "onWatchList": onWatchList,
                            "showComments": showComments,
                            "isOwner" : isOwner,
                            "bidError": bidError
                        })
                    else:
                        bidError = "Please enter a bid higher than the current highest bid."
                except ValueError:
                    bidError = "Invalid bid value. Please enter a valid number."

        return render(request, "auctions/product.html",{
            "product": productDetails,
            "msg": "Bid update FAILED.",
            "update": False,
            "onWatchList": onWatchList,
            "showComments": showComments,
            "isOwner" : isOwner,
            "bidError": bidError
        })
        
    return HttpResponseRedirect(reverse("product", args=[id]))


def newComment(request,id):
    theCurrentUser = request.user
    productDetails = Listing.objects.get(pk=id)
    msg = request.POST['newComment']
    
    newComment = Comment(
        writer = theCurrentUser,
        product = productDetails,
        msg = msg,
        timestamp = timezone.now()
    )
    newComment.save()
    return HttpResponseRedirect(reverse("product", args=[id]))

def toWatchList(request):
    if request.user.is_authenticated:
        theCurrentUser = request.user
        lists = theCurrentUser.WatchListForUsers.all()
        return render(request, "auctions/toWatchList.html", {
        "lists": lists
        })
    else:
        return render(request, "auctions/toWatchList.html")

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
        categoryForm = request.POST.get('category')
        if categoryForm:
            try:
                category = Category.objects.get(categoryName=categoryForm)
                activeList = Listing.objects.filter(isActive=True, category=category)
            except Category.DoesNotExist:
                activeList = Listing.objects.filter(isActive=True)
        else:
            activeList = Listing.objects.filter(isActive=True)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeList,
            "categories": categories,
            "selected_category": categoryForm
        })
    else:
        return HttpResponseRedirect(reverse("index"))




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
        
        bid = Bid(bid=int(price), user = thecurrentUser)
        bid.save()

        newListing= Listing(
            title = title,
            description = description,
            imgUrl = imgUrl,
            price = bid,
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
