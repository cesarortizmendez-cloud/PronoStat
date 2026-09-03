from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='regresion'),
    path('api/solve', views.solve_api, name='regresion_solve'),
    path('api/compare', views.compare_api, name='regresion_compare'),
]
