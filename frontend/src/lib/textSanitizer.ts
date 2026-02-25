const PLACEHOLDER_RE = /^(belirleniyor|undefined|loading\.\.\.|null|none|nan|veto edildi)$/i;

const ALLOWED_CHARS_RE = /[^0-9A-Za-zÇĞİÖŞÜçğıöşü\s.,;:!?\-_'"%&/+#@*()\[\]{}=<>|]/g;

export function sanitizeDisplayText(value: unknown, fallback = ''): string {
  if (value === null || value === undefined) return fallback;

  const text = String(value).trim();
  if (!text) return fallback;
  if (PLACEHOLDER_RE.test(text)) return fallback;

  const cleaned = text.replace(ALLOWED_CHARS_RE, '').replace(/\s{2,}/g, ' ').trim();
  if (!cleaned || PLACEHOLDER_RE.test(cleaned)) return fallback;

  return cleaned;
}

export function sanitizeDisplayList(values: unknown[], fallback = ''): string[] {
  return (values || [])
    .map((v) => sanitizeDisplayText(v, fallback))
    .filter((v) => !!v);
}
