from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='informes'),
    path('api/resumen', views.resumen_api, name='informes_resumen'),
]
