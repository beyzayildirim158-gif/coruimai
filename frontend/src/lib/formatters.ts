export const formatNumber = (value?: number | null, options: Intl.NumberFormatOptions = {}) => {
  if (value === undefined || value === null) return '—';
  return new Intl.NumberFormat('en-US', options).format(value);
};

export const formatPercentage = (value?: number | null, fractionDigits = 1) => {
  if (value === undefined || value === null) return '—';
  return `${value.toFixed(fractionDigits)}%`;
};

export const formatDateTime = (value?: string | Date | null) => {
  if (!value) return '—';
  const date = typeof value === 'string' ? new Date(value) : value;
  return date.toLocaleString('en-US', {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const gradeColor = (grade?: string | null) => {
  switch (grade) {
    case 'A':
      return 'text-emerald-300';
    case 'B':
      return 'text-lime-300';
    case 'C':
      return 'text-amber-300';
    case 'D':
      return 'text-orange-300';
    case 'F':
      return 'text-rose-400';
    default:
      return 'text-slate-400';
  }
};
