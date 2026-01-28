/**
 * Lightweight date formatting utilities (no deps).
 * - Accepts Date | number (ms) | string
 * - Formatting uses Intl.DateTimeFormat + formatToParts for stable tokens
 */

function toDate(input) {
  if (input instanceof Date) return new Date(input.getTime());
  if (typeof input === 'number') return new Date(input);
  if (typeof input === 'string') return new Date(input);
  return new Date(NaN);
}

function isValidDate(date) {
  return date instanceof Date && !Number.isNaN(date.getTime());
}

function pad2(value) {
  return String(value).padStart(2, '0');
}

function pad3(value) {
  return String(value).padStart(3, '0');
}

function getParts(dateInput, { locale = 'zh-CN', timeZone } = {}) {
  const date = toDate(dateInput);
  if (!isValidDate(date)) return null;

  const formatter = new Intl.DateTimeFormat(locale, {
    timeZone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });

  const parts = formatter.formatToParts(date);
  const map = Object.create(null);
  for (const part of parts) {
    if (part.type !== 'literal') map[part.type] = part.value;
  }

  const ms = date.getMilliseconds();
  map.millisecond = pad3(ms);
  return map;
}

/**
 * Format with a simple pattern.
 * Supported tokens: YYYY MM DD HH mm ss SSS
 */
function formatWithPattern(dateInput, pattern = 'YYYY-MM-DD', options) {
  const date = toDate(dateInput);
  if (!isValidDate(date)) return '';

  const parts = getParts(date, options);
  if (!parts) return '';

  return pattern
    .replaceAll('YYYY', parts.year)
    .replaceAll('MM', parts.month)
    .replaceAll('DD', parts.day)
    .replaceAll('HH', parts.hour)
    .replaceAll('mm', parts.minute)
    .replaceAll('ss', parts.second)
    .replaceAll('SSS', parts.millisecond);
}

function formatDate(dateInput, options) {
  return formatWithPattern(dateInput, 'YYYY-MM-DD', options);
}

function formatTime(dateInput, options) {
  return formatWithPattern(dateInput, 'HH:mm:ss', options);
}

function formatDateTime(dateInput, options) {
  return formatWithPattern(dateInput, 'YYYY-MM-DD HH:mm:ss', options);
}

function formatISODate(dateInput, options) {
  // Same as formatDate; kept for semantic clarity
  return formatDate(dateInput, options);
}

/**
 * Parse YYYY-MM-DD to a Date at local 00:00:00.
 */
function parseISODate(isoDateString) {
  if (typeof isoDateString !== 'string') return new Date(NaN);
  const match = /^\s*(\d{4})-(\d{2})-(\d{2})\s*$/.exec(isoDateString);
  if (!match) return new Date(NaN);
  const year = Number(match[1]);
  const monthIndex = Number(match[2]) - 1;
  const day = Number(match[3]);
  return new Date(year, monthIndex, day);
}

function startOfDay(dateInput) {
  const date = toDate(dateInput);
  if (!isValidDate(date)) return new Date(NaN);
  return new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0, 0);
}

function endOfDay(dateInput) {
  const date = toDate(dateInput);
  if (!isValidDate(date)) return new Date(NaN);
  return new Date(date.getFullYear(), date.getMonth(), date.getDate(), 23, 59, 59, 999);
}

function addDays(dateInput, days) {
  const date = toDate(dateInput);
  if (!isValidDate(date)) return new Date(NaN);
  const result = new Date(date.getTime());
  result.setDate(result.getDate() + Number(days));
  return result;
}

function addMinutes(dateInput, minutes) {
  const date = toDate(dateInput);
  if (!isValidDate(date)) return new Date(NaN);
  return new Date(date.getTime() + Number(minutes) * 60_000);
}

function addMonths(dateInput, months) {
  const date = toDate(dateInput);
  if (!isValidDate(date)) return new Date(NaN);
  const result = new Date(date.getTime());
  const originalDay = result.getDate();

  result.setDate(1);
  result.setMonth(result.getMonth() + Number(months));

  const lastDayOfTargetMonth = new Date(result.getFullYear(), result.getMonth() + 1, 0).getDate();
  result.setDate(Math.min(originalDay, lastDayOfTargetMonth));
  return result;
}

/**
 * Relative time like: "3分钟前" / "2天后"
 */
function formatRelativeTime(dateInput, {
  baseDate = new Date(),
  locale = 'zh-CN',
  numeric = 'auto',
} = {}) {
  const date = toDate(dateInput);
  const base = toDate(baseDate);
  if (!isValidDate(date) || !isValidDate(base)) return '';

  const diffMs = date.getTime() - base.getTime();
  const diffSeconds = Math.round(diffMs / 1000);

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric });
  const abs = Math.abs(diffSeconds);

  if (abs < 60) return rtf.format(diffSeconds, 'second');

  const diffMinutes = Math.round(diffSeconds / 60);
  if (Math.abs(diffMinutes) < 60) return rtf.format(diffMinutes, 'minute');

  const diffHours = Math.round(diffMinutes / 60);
  if (Math.abs(diffHours) < 24) return rtf.format(diffHours, 'hour');

  const diffDays = Math.round(diffHours / 24);
  if (Math.abs(diffDays) < 30) return rtf.format(diffDays, 'day');

  const diffMonths = Math.round(diffDays / 30);
  if (Math.abs(diffMonths) < 12) return rtf.format(diffMonths, 'month');

  const diffYears = Math.round(diffMonths / 12);
  return rtf.format(diffYears, 'year');
}

module.exports = {
  toDate,
  isValidDate,
  pad2,
  formatWithPattern,
  formatDate,
  formatTime,
  formatDateTime,
  formatISODate,
  parseISODate,
  startOfDay,
  endOfDay,
  addDays,
  addMinutes,
  addMonths,
  formatRelativeTime,
};
