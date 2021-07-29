from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("dla-tworcow/", views.ForCreators.as_view(), name="for-creators"),
    path("dla-organizacji/", views.ForOrganizations.as_view(), name="for-organizations"),
    path("zaloguj/", views.Login.as_view(), name="login"),
    path("zarejestruj/", views.Register.as_view(), name="register"),
    path("zarejestruj/tworca/", views.RegisterCreator.as_view(), name="register-creator"),
    path("zarejestruj/organizacja/", views.RegisterOrganization.as_view(), name="register-organization"),
    path("wyloguj/", views.Logout.as_view(), name="logout"),
]