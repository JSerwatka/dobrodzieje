from django.urls import path
from . import views

app_name = 'webapp'
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("dla-tworcow/", views.ForCreators.as_view(), name="for-creators"),
    path("dla-organizacji/", views.ForOrganizations.as_view(), name="for-organizations"),
    path("przegladaj-ogloszenia/", views.AnnouncementList.as_view(), name="announcement-list"),
    path("moje-ogloszenie/", views.MyAnnouncement.as_view(), name="my-announcement"),
    path("ogloszenie/<int:id>/", views.AnnouncementDetails.as_view(), name="announcement-detail"),
    path("stworz-ogloszenie/", views.AnnouncementCreate.as_view(), name="announcement-create"),
    path("edytuj-ogłoszenie/", views.AnnouncementUpdate.as_view(), name="announcement-edit"),
    path("usun-ogłoszenie/", views.AnnouncementDelete.as_view(), name="announcement-delete"),
    path("moje-druzyny/", views.MyTeams.as_view(), name="my-teams"),
    path("edytuj-profil/", views.EditProfile.as_view(), name="edit-profile"),
    path("zaloguj/", views.Login.as_view(), name="login"),
    path("zarejestruj/", views.Register.as_view(), name="register"),
    path("zarejestruj/tworca/", views.RegisterCreator.as_view(), name="register-creator"),
    path("zarejestruj/organizacja/", views.RegisterOrganization.as_view(), name="register-organization"),
    path("wyloguj/", views.Logout.as_view(), name="logout"),
]