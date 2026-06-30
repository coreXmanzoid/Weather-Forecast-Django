from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginUser, name="login"),
    path("signup/", views.signup, name="signup"),
    path("home", views.home, name="home"),
    path("logout", views.logoutUser, name="logout"),
    path("delete", views.deleteUser, name="deleteUser"),
    path("update-email-settings/", views.update_email_settings, name="update_email_settings"),
]
