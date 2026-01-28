const {
	formatDate,
	formatDateTime,
	formatTime,
	formatWithPattern,
	formatRelativeTime,
	parseISODate,
	addDays,
} = require('./dateUtils');

const now = new Date();

console.log('formatDate:', formatDate(now));
console.log('formatTime:', formatTime(now));
console.log('formatDateTime:', formatDateTime(now));
console.log('pattern:', formatWithPattern(now, 'YYYY/MM/DD HH:mm:ss.SSS'));

const d = parseISODate('2026-01-28');
console.log('parseISODate +1day:', formatDate(addDays(d, 1)));

console.log('relative (-3min):', formatRelativeTime(addDays(now, 0), { baseDate: new Date(now.getTime() + 3 * 60_000) }));

