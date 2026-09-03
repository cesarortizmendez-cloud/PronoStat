"""
PronoStat — Enrutador raíz. Incluye cada módulo (app) y las rutas PWA.
"""
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import never_cache
from django.conf import settings
import os


_MANIFEST = '''{
  "name": "PronoStat - Analisis de Datos y Pronosticos",
  "short_name": "PronoStat",
  "description": "Laboratorio educativo de estadistica, series de tiempo y pronosticos.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#f1f5f9",
  "theme_color": "#0f766e",
  "lang": "es",
  "icons": []
}'''

_SERVICE_WORKER = '''
self.addEventListener("install", function(e){ self.skipWaiting(); });
self.addEventListener("activate", function(e){ self.clients.claim(); });
self.addEventListener("fetch", function(e){
  var req = e.request;
  if (req.method !== "GET") return;
  e.respondWith(fetch(req).catch(function(){ return caches.match(req); }));
});
'''


@never_cache
def manifest(request):
    return HttpResponse(_MANIFEST, content_type='application/manifest+json')


@never_cache
def service_worker(request):
    resp = HttpResponse(_SERVICE_WORKER, content_type='application/javascript')
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
