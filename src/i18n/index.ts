import translations, { type Locale } from './translations';

export function getTranslation(locale: Locale = 'en') {
  return translations[locale];
}

export function getLocaleFromUrl(url: URL): Locale {
  const pathname = url.pathname;
  if (pathname.startsWith('/es/') || pathname === '/es') return 'es';
  return 'en';
}

export function getLocalizedPath(path: string, locale: Locale): string {
  if (locale === 'en') return path;
  return `/es${path}`;
}

export function getOppositeLocalePath(url: URL): string {
  const locale = getLocaleFromUrl(url);
  const pathname = url.pathname;

  if (locale === 'es') {
    // Remove /es prefix
    let clean = pathname.replace(/^\/es/, '') || '/';
    // Remove -es suffix from slugs for properties and blog posts
    clean = clean.replace(/-es\/$/, '/');
    return clean;
  }

  // Switching EN → ES: add /es prefix and -es suffix for properties/blog
  if (pathname.match(/^\/(properties|blog)\//) && pathname !== '/properties/' && pathname !== '/blog/') {
    // Add -es before the trailing slash
    const esPath = pathname.replace(/\/$/, '-es/');
    return `/es${esPath}`;
  }

  return `/es${pathname}`;
}

export { type Locale };