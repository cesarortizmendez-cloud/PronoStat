from django.urls import path
from . import views

urlpatterns = [
    path('dataset', views.dataset, name='export_dataset'),
    path('descriptiva', views.descriptiva, name='export_descriptiva'),
    path('regresion', views.regresion, name='export_regresion'),
    path('pronostico', views.pronostico, name='export_pronostico'),
    path('econometria', views.econometria, name='export_econometria'),
    path('informe', views.informe, name='export_informe'),
]
