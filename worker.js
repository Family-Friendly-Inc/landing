// Cloudflare Worker. Static files are served straight from _site; wrangler.jsonc
// routes only /games/nogglets/daily* here (run_worker_first).
// ponytail: 7-digit cap on N (~27,000 years of Dailies); raise it if that ever matters.
const DAILY = /^\/games\/nogglets\/daily\/([1-9]\d{0,6})\/?$/;

export default {
  async fetch(request, env) {
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response(null, { status: 405, headers: { allow: "GET, HEAD" } });
    }
    const m = new URL(request.url).pathname.match(DAILY);
    const tpl = m && (await env.ASSETS.fetch(new URL("/games/nogglets/daily/", request.url)));
    if (!tpl || !tpl.ok) {
      const page = await env.ASSETS.fetch(new URL("/404", request.url));
      return new Response(page.body, { status: 404, headers: page.headers });
    }
    // N is digits only (regex above), so plain substitution is safe in HTML and URLs.
    const html = (await tpl.text()).replaceAll("{{N}}", m[1]);
    return new Response(html, {
      headers: {
        "content-type": "text/html; charset=utf-8",
        "cache-control": "public, max-age=3600",
        "x-content-type-options": "nosniff",
        "referrer-policy": "strict-origin-when-cross-origin",
      },
    });
  },
};
