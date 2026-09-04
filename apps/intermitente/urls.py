from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='intermitente'),
    path('api/run', views.run_api, name='intermitente_run'),
    path('api/comparar', views.comparar_api, name='intermitente_comparar'),
]
