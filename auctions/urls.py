from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("viewCategory", views.viewCategory, name="viewCategory"),
    path("product/<int:id>", views.product, name="product"),
    path("removeFromWatchList/<int:id>", views.removeFromWatchList, name="removeFromWatchList"),
    path("addToWatchList/<int:id>", views.addToWatchList, name="addToWatchList")
]
