import fs from 'node:fs';
import path from 'node:path';

import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// ---------------------------------------------------------------------------
// Sitemap exclusions — hidden property listings
// ---------------------------------------------------------------------------
// Properties marked `hidden: true` (sold / rented / deliberately unlisted) are
// still built as pages, but they appear in NO listing page: both /properties/
// and /es/properties/ filter them out with `!p.data.hidden`. That makes them
// ORPHANS — reachable only by direct URL, linked from nowhere on the site.
//
// Submitting an orphan to Google asks it to crawl and index a page that:
//   • has no internal links pointing at it, and
//   • advertises a property that is no longer available.
//
// 16 listings were being submitted this way before this filter was added
// (2026-09-16). They stay reachable so existing shared links keep working, and
// their templates now emit `noindex, follow` — this filter keeps them out of
// the sitemap.
//
// The list is derived from the content files at build time, so marking a
// property `hidden: true` (or removing that flag) is enough — no list to
// maintain here.
function hiddenPropertySlugs() {
  const dir = path.join(process.cwd(), 'src', 'content', 'properties');
  try {
    return new Set(
      fs
        .readdirSync(dir)
        .filter((f) => f.endsWith('.md'))
        .filter((f) => /^hidden:\s*true\s*$/m.test(fs.readFileSync(path.join(dir, f), 'utf8')))
        .map((f) => f.replace(/\.md$/, '')),
    );
  } catch {
    return new Set();
  }
}

const HIDDEN_PROPERTIES = hiddenPropertySlugs();

export default defineConfig({
  site: 'https://antiguarealestatedevelopment.com',
  output: 'static',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      filter: (page) => {
        // Matches /properties/<slug>/ and /es/properties/<slug>/
        const m = page.match(/\/(?:es\/)?properties\/([^/]+)\/?$/);
        return !(m && HIDDEN_PROPERTIES.has(m[1]));
      },
    }),
  ],
  build: {
    inlineStylesheets: 'auto',
  },
  vite: {
    build: {
      cssMinify: true,
    },
  },
  i18n: {
    locales: ['en', 'es'],
    defaultLocale: 'en',
    routing: {
      prefixDefaultLocale: false,
      redirectToDefaultLocale: false,
    },
  },
});
