from django.urls import path
from vaccine import views

app_name = "vaccine"

urlpatterns = [
    path("", views.VaccineList.as_view(), name="list"),
    path("<int:id>/", views.VaccineDetail.as_view(), name="detail"),
    path("create/", views.CreateVaccine.as_view(), name="create"),
    path("update/<int:id>/", views.UpdateVaccine.as_view(), name="update"),
    path("delete/<int:id>/", views.DeleteVaccine.as_view(), name="delete"),
]