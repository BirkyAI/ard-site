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
});