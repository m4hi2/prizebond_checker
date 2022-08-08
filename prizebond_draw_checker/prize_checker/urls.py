from django.urls import path

from . import views

urlpatterns = [
    path("profile", views.profile),
    path("add", views.add_prize_bond_number)
]