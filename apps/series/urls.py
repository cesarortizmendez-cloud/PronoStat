from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='series'),
    path('api/descomponer', views.descomponer_api, name='series_descomponer'),
    path('api/acf', views.acf_api, name='series_acf'),
    path('api/estacionariedad', views.estacionariedad_api, name='series_estacionariedad'),
]
