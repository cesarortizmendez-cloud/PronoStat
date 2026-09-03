"""
PronoStat — Enrutador raíz. Incluye cada módulo (app) y las rutas PWA.
"""
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import never_cache
from django.conf import settings
import os


def _read_static(rel_path):
    full = os.path.join(settings.BASE_DIR, 'static', rel_path)
    with open(full, 'r', encoding='utf-8') as f:
        return f.read()


@never_cache
def manifest(request):
    return HttpResponse(_read_static('manifest.json'), content_type='application/manifest+json')


@never_cache
def service_worker(request):
    resp = HttpResponse(_read_static('service-worker.js'), content_type='application/javascript')
    resp['Service-Worker-Allowed'] = '/'
    return resp


def healthz(request):
    return JsonResponse({'status': 'ok', 'app': 'PronoStat', 'version': '1.0'})


urlpatterns = [
    path('', include('apps.home.urls')),
    path('datos/', include('apps.datos.urls')),
    path('descriptiva/', include('apps.descriptiva.urls')),
    path('regresion/', include('apps.regresion.urls')),
    path('pronostico/', include('apps.pronostico.urls')),
    path('exportar/', include('apps.exportar.urls')),
    # PWA
    path('manifest.json', manifest, name='manifest'),
    path('service-worker.js', service_worker, name='service_worker'),
    path('healthz', healthz, name='healthz'),
]
