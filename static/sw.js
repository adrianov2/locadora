self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  self.clients.claim();
});

// Sem cache de dados porque o app depende do PostgreSQL sempre online.
// Isso aqui só habilita o "Adicionar à tela inicial / Instalar app".
self.addEventListener('fetch', (e) => {
  e.respondWith(fetch(e.request));
});

