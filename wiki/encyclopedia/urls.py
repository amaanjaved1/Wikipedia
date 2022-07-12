from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("random", views.rand_select, name="random")
]
