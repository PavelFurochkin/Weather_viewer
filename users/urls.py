from django.urls import path
from .views import UserRegistration, UserLogin, LogoutUser

app_name = 'users'

urlpatterns = [
    path("registration", UserRegistration.as_view(), name="registration"),
    path("login", UserLogin.as_view(), name="login"),
    path("logout", LogoutUser.as_view(), name="logout"),

]