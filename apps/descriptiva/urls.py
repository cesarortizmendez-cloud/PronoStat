from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='descriptiva'),
    path('api/solve', views.solve_api, name='descriptiva_solve'),
    path('api/explore', views.explore_api, name='descriptiva_explore'),
]
