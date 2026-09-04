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
var CACHE = "pronostat-v2";
self.addEventListener("install", function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){ return c.addAll(["/"]); }).catch(function(){}));
  self.skipWaiting();
});
self.addEventListener("activate", function(e){
  e.waitUntil(caches.keys().then(function(ks){ return Promise.all(ks.filter(function(k){return k!==CACHE;}).map(function(k){return caches.delete(k);})); }));
  self.clients.claim();
});
self.addEventListener("fetch", function(e){
  var req = e.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (req.mode === "navigate") {
    e.respondWith(fetch(req).then(function(res){ var cp=res.clone(); caches.open(CACHE).then(function(c){c.put(req,cp);}); return res; }).catch(function(){ return caches.match(req).then(function(r){ return r || caches.match("/"); }); }));
    return;
  }
  e.respondWith(caches.match(req).then(function(r){ return r || fetch(req).then(function(res){ var cp=res.clone(); caches.open(CACHE).then(function(c){c.put(req,cp);}); return res; }).catch(function(){ return r; }); }));
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
    path('muestreo/', include('apps.muestreo.urls')),
    path('descriptiva/', include('apps.descriptiva.urls')),
    path('regresion/', include('apps.regresion.urls')),
    path('pronostico/', include('apps.pronostico.urls')),
    path('inferencia/', include('apps.inferencia.urls')),
    path('econometria/', include('apps.econometria.urls')),
    path('series/', include('apps.series.urls')),
    path('arima/', include('apps.arima.urls')),
    path('sarimax/', include('apps.sarimax.urls')),
    path('intermitente/', include('apps.intermitente.urls')),
    path('ensamble/', include('apps.ensamble.urls')),
    path('multiple/', include('apps.multiple.urls')),
    path('jerarquico/', include('apps.jerarquico.urls')),
    path('simulacion/', include('apps.simulacion.urls')),
    path('informes/', include('apps.informes.urls')),
    path('pwa/', include('apps.pwa.urls')),
    path('exportar/', include('apps.exportar.urls')),
    # PWA
    path('manifest.json', manifest, name='manifest'),
    path('service-worker.js', service_worker, name='service_worker'),
    path('healthz', healthz, name='healthz'),
]
