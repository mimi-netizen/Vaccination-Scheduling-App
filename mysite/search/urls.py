from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_view, name='search'),
    path('api/nearby-centers/', views.nearby_centers_api, name='nearby-centers-api'),
    path('api/vaccine-availability/', views.vaccine_availability_api, name='vaccine-availability-api'),
]
