from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='muestreo'),
    path('api/extraer', views.extraer_api, name='muestreo_extraer'),
    path('api/tam-media', views.tam_media_api, name='muestreo_tam_media'),
    path('api/tam-prop', views.tam_prop_api, name='muestreo_tam_prop'),
    path('api/asignacion', views.asignacion_api, name='muestreo_asignacion'),
    path('api/estimar-srs', views.estimar_srs_api, name='muestreo_estimar_srs'),
    path('api/estimar-estr', views.estimar_estr_api, name='muestreo_estimar_estr'),
]
