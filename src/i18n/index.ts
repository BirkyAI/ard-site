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
    const clean = pathname.replace(/^\/es/, '') || '/';
    return clean;
  }
  // Add /es prefix
  return `/es${pathname}`;
}

export { type Locale };
