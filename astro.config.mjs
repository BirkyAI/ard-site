import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://antiguarealestatedevelopment.com',
  output: 'static',
  trailingSlash: 'always',
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
