from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='descriptiva'),
    path('api/solve', views.solve_api, name='descriptiva_solve'),
    path('api/explore', views.explore_api, name='descriptiva_explore'),
    path('api/tabla', views.tabla_api, name='descriptiva_tabla'),
    path('api/tabla-doble', views.tabla_doble_api, name='descriptiva_tabla_doble'),
]
