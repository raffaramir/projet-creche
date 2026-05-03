/* Little Future — Service Worker
 * Strategy:
 *   - Precache app shell (static assets + offline fallback) on install.
 *   - Static (CSS/JS/img/font): cache-first, fall back to network.
 *   - Navigations (HTML): network-first with offline.html fallback.
 *   - API (/api/v1/): network-only (always fresh, no stale data).
 */

const VERSION = "lf-v1";
const STATIC_CACHE  = `${VERSION}-static`;
const RUNTIME_CACHE = `${VERSION}-runtime`;

const PRECACHE_URLS = [
    "/",
    "/hors-ligne/",
    "/static/css/main.css",
    "/static/js/main.js",
    "/static/img/favicon.png",
    "/static/img/pwa/icon-192.png",
    "/static/img/pwa/icon-512.png",
    "/static/manifest.webmanifest",
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(STATIC_CACHE).then((cache) => cache.addAll(PRECACHE_URLS))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys
                    .filter((k) => k !== STATIC_CACHE && k !== RUNTIME_CACHE)
                    .map((k) => caches.delete(k))
            )
        ).then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (event) => {
    const req = event.request;
    if (req.method !== "GET") return;

    const url = new URL(req.url);

    // Same-origin only
    if (url.origin !== self.location.origin) return;

    // API: always fresh
    if (url.pathname.startsWith("/api/")) {
        event.respondWith(fetch(req).catch(() => new Response(
            JSON.stringify({ detail: "Hors-ligne" }),
            { status: 503, headers: { "Content-Type": "application/json" } }
        )));
        return;
    }

    // Admin: bypass SW entirely
    if (url.pathname.startsWith("/admin/")) return;

    // HTML navigations: network-first, fall back to offline page
    if (req.mode === "navigate" || (req.headers.get("Accept") || "").includes("text/html")) {
        event.respondWith(
            fetch(req)
                .then((res) => {
                    const copy = res.clone();
                    caches.open(RUNTIME_CACHE).then((cache) => cache.put(req, copy));
                    return res;
                })
                .catch(() =>
                    caches.match(req)
                        .then((cached) => cached || caches.match("/hors-ligne/"))
                )
        );
        return;
    }

    // Static assets: cache-first
    if (url.pathname.startsWith("/static/") || url.pathname.startsWith("/media/")) {
        event.respondWith(
            caches.match(req).then((cached) => cached || fetch(req).then((res) => {
                const copy = res.clone();
                caches.open(STATIC_CACHE).then((cache) => cache.put(req, copy));
                return res;
            }))
        );
        return;
    }
});

// Listen for skipWaiting messages from the page
self.addEventListener("message", (event) => {
    if (event.data === "SKIP_WAITING") self.skipWaiting();
});
