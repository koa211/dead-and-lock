from django.urls import path

from . import views

app_name = "ranks"
urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("<int:match_id>/", views.daily, name="daily"),
]
