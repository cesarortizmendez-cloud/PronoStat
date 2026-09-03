/* PronoStat — Service Worker (cache básico para funcionamiento offline del cascarón).
   V1: cache-first para estáticos, network-first para navegación. */
const CACHE = 'pronostat-v1';
const CORE = [
  '/',
  '/static/css/pronostat.css',
  '/static/js/data-store.js',
  '/static/js/pwa-install.js',
  '/static/icons/icon-192.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).catch(() => {}));
  self.skipWaiting();
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) =>
    Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;                 // no cachear POST (APIs)
  const url = new URL(req.url);
  if (url.pathname.startsWith('/static/')) {
    e.respondWith(caches.match(req).then((r) => r || fetch(req).then((res) => {
      const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); return res;
    })));
  } else {
    e.respondWith(fetch(req).catch(() => caches.match(req).then((r) => r || caches.match('/'))));
  }
});
