from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("dla-tworcow/", views.ForCreators.as_view(), name="dla-tworcow"),
    path("dla-organizacji/", views.ForOrganizations.as_view(), name="dla-organizacji"),
]