self.__precacheManifest = [].concat(self.__precacheManifest || [])
// workbox.precaching.suppressWarnings()
workbox.precaching.precacheAndRoute(self.__precacheManifest, {})

workbox.routing.registerRoute(
  /https:\/\/admin-grupo24.proyecto2021.linti.unlp.edu.ar\/api\/.*/,
  workbox.strategies.networkFirst({
    cacheName: 'inundasafe-api-cache',
    plugins: [
      new workbox.expiration.Plugin({
        maxEntries: 600,
        maxAgeSeconds: 1200
      }),
      new workbox.cacheableResponse.Plugin({
        statuses: [0, 200]
      }),
    ]
  })
)

// install new service worker when ok, then reload page.
self.addEventListener('message', (msg) => {
  if (msg.data.action == 'skipWaiting') {
    self.skipWaiting()
  }
})
