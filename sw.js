// Forge2Forge app: keeps the site loading fast and working with a weak connection.
// Pages always load fresh from forge2forge.com when online, so the app shows site updates right away.
// When icons or images change, bump the CACHE number below so phones fetch the new ones.
// It also receives the new-episode notifications (OneSignal).
try { importScripts('https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js'); } catch (e) {}
const CACHE = 'f2f-v11';
const SHELL = ['./', './index.html', './manifest.webmanifest', './forge-bg-poster.jpg',
  './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png', './icons/qr.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;   // YouTube etc. go straight to the network
  if (url.pathname.endsWith('.mp4')) return;                              // background video streams normally
  if (url.pathname.endsWith('version.json')) return;                      // version check always goes to the live site
  if (req.mode === 'navigate') {                                          // pages: newest version first, cached copy if offline
    e.respondWith(fetch(req.url, { cache: 'no-cache', credentials: 'same-origin' }).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put('./index.html', c)); return r; })
      .catch(() => caches.match('./index.html')));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {    // images/icons: cached copy first
    if (r.ok) { const c = r.clone(); caches.open(CACHE).then(x => x.put(req, c)); }
    return r;
  })));
});
