from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pronostico'),
    path('api/solve', views.solve_api, name='pronostico_solve'),
    path('api/compare', views.compare_api, name='pronostico_compare'),
]
