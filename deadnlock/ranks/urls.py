from django.urls import path

from . import views

app_name = "match"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:match_id>/", views.daily, name="daily"),
]
