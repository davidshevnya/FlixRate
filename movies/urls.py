from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/<slug:slug>/", views.detail, name="detail")
]
