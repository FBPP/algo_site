from django.urls import path, include

from . import views

app_name = "register"
urlpatterns = [
    path("", views.regist, name = "regist"),
    path("confirm/<uuid:code>", views.confirm, name = "confirm"),
    path("lg/", views.lg, name = "lg"),
]