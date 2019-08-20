from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="shophome"),
    path('about/', views.about,name="about"),
    path('contact/', views.contact,name="contact"),
    path('tracker', views.tracker,name="track"),
    path('search/', views.search,name="search"),
    path('productview/<int:myid>', views.productview,name="product"),
    path('checkout/', views.checkout,name="check"),
    #path('handlerequest/', views.handlerequest,name="handlerequest"),
]