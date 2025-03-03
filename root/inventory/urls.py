from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_hosts/", views.all_hosts, name="all_hosts"),
    path("view_host/<id>/", views.view_host, name="view_host"),
    path("view_domain/<domid>/<physicalhostid>/", views.view_domain, name="view_domain"),
]
