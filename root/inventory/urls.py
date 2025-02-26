from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("view_host/<int:id>/", views.view_host, name="view_host"),
]
