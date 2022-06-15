from . import views
from django.urls import path,include

urlpatterns = [
    path("", views.index),
    path("products/<int:myid>",views.productpage,name="product"),
    path("allproduct/<str:name>",views.allproducts),
    path("contact/",views.contact),
    path("checkoutpage/",views.checkoutpage),
    path("tracker/",views.tracker),
    path("search/",views.search),
    path("signup/",views.handlesignup),
    path("login/",views.handlelogin),
    path("logout/",views.handlelogout),
]