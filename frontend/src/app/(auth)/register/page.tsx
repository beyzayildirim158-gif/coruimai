"use client";

import Link from 'next/link';
import { RadarIcon } from '@/components/icons';

const WHATSAPP_NUMBER = '905346116167'; // buraya numarayı yaz
const WHATSAPP_MESSAGE = encodeURIComponent(
  'Merhaba, corium.ai platformuna erişim almak istiyorum. Kullanıcı hesabı oluşturabilir misiniz?'
);
const WHATSAPP_URL = `https://wa.me/${WHATSAPP_NUMBER}?text=${WHATSAPP_MESSAGE}`;

export default function RegisterPage() {
  return (
    <div className="flex w-full max-w-5xl flex-col gap-10 lg:flex-row">
      {/* Sol panel */}
      <div className="flex flex-1 flex-col gap-6 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex items-center gap-3 text-sm uppercase tracking-[0.3em] text-primary">
          <RadarIcon size={20} />
          corium.ai Platform
        </div>
        <h1 className="text-4xl font-bold text-slate-900">AI destekli Instagram analiz platformu</h1>
        <p className="max-w-md text-slate-600">
          7 yapay zeka ajanı, gerçek zamanlı Instagram verisi ve kapsamlı raporlama sistemi.
        </p>
        <ul className="space-y-3 text-sm text-slate-700">
          <li className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-primary" /> 7 AI uzmanı FastAPI üzerinden orkestrasyon
          </li>
          <li className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-trust" /> Apify ile canlı Instagram verisi
          </li>
          <li className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-primary" /> Stripe entegrasyonlu katmanlı abonelik
          </li>
        </ul>
      </div>

      {/* Sağ panel — WhatsApp */}
      <div className="flex flex-1 flex-col items-center justify-center gap-6 rounded-3xl border border-slate-200 bg-white p-10 shadow-lg text-center">
        {/* WhatsApp ikonu */}
        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[#25D366]/10">
          <svg viewBox="0 0 24 24" className="h-10 w-10 fill-[#25D366]">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
            <path d="M12 0C5.373 0 0 5.373 0 12c0 2.124.554 4.118 1.523 5.849L.057 23.535a.75.75 0 0 0 .916.919l5.733-1.498A11.943 11.943 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.75a9.721 9.721 0 0 1-4.964-1.362l-.355-.212-3.686.964.983-3.595-.232-.371A9.712 9.712 0 0 1 2.25 12C2.25 6.615 6.615 2.25 12 2.25S21.75 6.615 21.75 12 17.385 21.75 12 21.75z"/>
          </svg>
        </div>

        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Erişim talebi</p>
          <h2 className="mt-2 text-3xl font-semibold text-slate-900">Hesap oluşturmak için</h2>
          <h2 className="text-3xl font-semibold text-[#25D366]">WhatsApp'tan ulaşın</h2>
        </div>

        <p className="max-w-xs text-slate-600">
          Yeni kullanıcı hesapları manuel olarak oluşturulmaktadır. Aşağıdaki butona tıklayarak
          bizimle WhatsApp üzerinden iletişime geçin, kullanıcı adı ve şifrenizi iletelim.
        </p>

        <a
          href={WHATSAPP_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="flex w-full items-center justify-center gap-3 rounded-2xl bg-[#25D366] px-6 py-4 text-lg font-semibold text-white shadow-md transition-all hover:bg-[#1ebe5d] active:scale-95"
        >
          <svg viewBox="0 0 24 24" className="h-6 w-6 fill-white">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
            <path d="M12 0C5.373 0 0 5.373 0 12c0 2.124.554 4.118 1.523 5.849L.057 23.535a.75.75 0 0 0 .916.919l5.733-1.498A11.943 11.943 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.75a9.721 9.721 0 0 1-4.964-1.362l-.355-.212-3.686.964.983-3.595-.232-.371A9.712 9.712 0 0 1 2.25 12C2.25 6.615 6.615 2.25 12 2.25S21.75 6.615 21.75 12 17.385 21.75 12 21.75z"/>
          </svg>
          WhatsApp ile Kayıt İste
        </a>

        <div className="w-full rounded-2xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-500">
          🔒 Hesap bilgileriniz size özel olarak iletilecektir.
        </div>

        <p className="text-sm text-slate-500">
          Zaten hesabınız var mı?{' '}
          <Link href="/login" className="font-medium text-primary hover:text-primary/80">
            Giriş yapın
          </Link>
        </p>
      </div>
    </div>
  );
}
