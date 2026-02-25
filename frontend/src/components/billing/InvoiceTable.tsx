import Link from 'next/link';
import { formatDateTime } from '@/lib/formatters';
import { ReceiptTextIcon } from '@/components/icons';

type Invoice = {
  id: string;
  number?: string | null;
  amount: number;
  currency: string;
  status?: string | null;
  paidAt?: string | null;
  pdfUrl?: string | null;
  hostedUrl?: string | null;
};

interface InvoiceTableProps {
  invoices?: Invoice[];
}

const statusStyles: Record<string, string> = {
  paid: 'text-emerald-600',
  open: 'text-amber-600',
  draft: 'text-slate-500',
  void: 'text-slate-400',
  uncollectible: 'text-red-600',
};

export function InvoiceTable({ invoices = [] }: InvoiceTableProps) {
  if (!invoices.length) {
    return (
      <div className="rounded-3xl border border-dashed border-slate-200 bg-slate-50 p-8 text-center text-slate-500">
        <ReceiptTextIcon className="mx-auto mb-3 text-primary-500" size={32} />
        No invoices yet.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
      <div className="grid grid-cols-[1.5fr_1fr_1fr_120px] gap-4 bg-slate-50 px-6 py-3 text-xs uppercase tracking-[0.2em] text-slate-500 max-sm:hidden">
        <span>Invoice</span>
        <span>Amount</span>
        <span>Date</span>
        <span className="text-right">Actions</span>
      </div>
      <div className="divide-y divide-slate-100 text-sm text-slate-900">
        {invoices.map((invoice) => (
          <div key={invoice.id} className="grid grid-cols-1 gap-4 px-6 py-4 sm:grid-cols-[1.5fr_1fr_1fr_120px]">
            <div>
              <p className="font-semibold text-slate-900">{invoice.number ?? invoice.id}</p>
              <p className={statusStyles[invoice.status ?? ''] ?? 'text-slate-500'}>
                {invoice.status?.toUpperCase() ?? 'UNKNOWN'}
              </p>
            </div>
            <div className="text-slate-700">
              ${(invoice.amount ?? 0).toFixed(2)} {invoice.currency}
            </div>
            <div className="text-slate-500">{formatDateTime(invoice.paidAt)}</div>
            <div className="flex items-center justify-end gap-2 text-xs">
              {invoice.hostedUrl && (
                <Link href={invoice.hostedUrl} target="_blank" className="rounded-2xl border border-slate-200 px-3 py-1 text-slate-700 hover:bg-slate-50">
                  View
                </Link>
              )}
              {invoice.pdfUrl && (
                <Link href={invoice.pdfUrl} target="_blank" className="rounded-2xl border border-slate-200 px-3 py-1 text-slate-700 hover:bg-slate-50">
                  PDF
                </Link>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
