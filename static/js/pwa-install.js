/* PronoStat — instalación PWA + registro del service worker */
(function () {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/service-worker.js').catch(() => {});
    });
  }
  let deferred = null;
  const btn = document.getElementById('pwa-install');
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferred = e;
    if (btn) btn.hidden = false;
  });
  if (btn) {
    btn.addEventListener('click', async () => {
      if (!deferred) {
        // iOS: no soporta beforeinstallprompt
        alert('En iPhone/iPad: abre en Safari → Compartir → “Agregar a pantalla de inicio”.');
        return;
      }
      deferred.prompt();
      await deferred.userChoice;
      deferred = null;
      btn.hidden = true;
    });
  }
  window.addEventListener('appinstalled', () => { if (btn) btn.hidden = true; });
})();
