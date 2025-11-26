const CACHE_NAME = 'fair-discovery-v3'; // Version bump forces update

// Install: Activate immediately (Don't wait)
self.addEventListener('install', event => {
  self.skipWaiting(); 
});

// Activate: Delete old caches immediately
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  return self.clients.claim(); // Take control of the page now
});

// Fetch Strategy: NETWORK FIRST, CACHE FALLBACK
// This ensures users always see the live site.
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // If we are online and found the file, return it!
        return response;
      })
      .catch(() => {
        // If we are offline, try to find it in the cache
        return caches.match(event.request);
      })
  );
});
