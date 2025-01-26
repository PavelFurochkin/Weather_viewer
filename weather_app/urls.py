from django.urls import path

from .views import StartPage, SearchPage

app_name = "weather_app"
urlpatterns = [
    path("", StartPage.as_view(), name="main"),
    path("search/", SearchPage.as_view(), name="search"),
]
