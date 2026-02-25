'use client';

import React, { useState } from 'react';
import { 
  BookOpenIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  MagnifyingGlassIcon,
} from '@heroicons/react/24/outline';
import { useTranslation } from '@/i18n/TranslationProvider';

export interface GlossaryTerm {
  term: string;
  simpleExplanation: string;
  category?: string;
  example?: string;
}

// Default glossary terms in Turkish - Comprehensive and educational
export const defaultGlossaryTerms: GlossaryTerm[] = [
  // === ENGAGEMENT METRICS (Etkileşim Metrikleri) ===
  {
    term: 'Engagement Rate',
    simpleExplanation: 'Takipçilerinizin içeriklerinizle ne kadar etkileşime girdiğini gösteren kritik metrik. Beğeni, yorum, kaydetme ve paylaşımların toplam takipçi sayısına oranıdır. %3-6 arası iyi, %6+ mükemmeldir. Düşük oran, içerik-kitle uyumsuzluğuna işaret eder.',
    category: 'Metrikler',
    example: '%3.5 engagement rate = Her 100 takipçiden ortalama 3-4 kişi içeriğinizle aktif etkileşime giriyor demektir',
  },
  {
    term: 'Reach',
    simpleExplanation: 'İçeriğinizi kaç farklı benzersiz kişinin gördüğünü gösterir. Aynı kişi 10 kez görse bile 1 reach sayılır. Takipçi sayınızın %20-30\'una ulaşıyorsanız iyi, %50+ mükemmeldir. Düşük reach, algoritmanın içeriğinizi öne çıkarmadığı anlamına gelir.',
    category: 'Metrikler',
    example: '10K reach = 10.000 farklı gerçek kişi içeriğinizi gördü',
  },
  {
    term: 'Impressions',
    simpleExplanation: 'İçeriğinizin toplam görüntülenme sayısı. Aynı kişi birden fazla kez görebilir. Impressions/Reach oranı içeriğin tekrar görülme değerini gösterir. Yüksek oran = insanlar içeriğe geri dönüyor demektir.',
    category: 'Metrikler',
    example: 'Reach: 5.000, Impressions: 8.000 = Her kişi ortalama 1.6 kez gördü (içerik ilgi çekici)',
  },
  {
    term: 'Save Rate',
    simpleExplanation: 'İçeriğinizi kaç kişinin koleksiyonuna kaydettiğini gösterir. En değerli etkileşim türüdür çünkü kullanıcı "buna tekrar bakmak istiyorum" diyor. Yüksek save rate = içerik gerçekten değerli ve eğitici. Algoritma bu içeriği çok sever.',
    category: 'Metrikler',
    example: '%2+ save rate harika performans, özellikle carousel ve eğitim içeriklerinde',
  },
  {
    term: 'Share Rate',
    simpleExplanation: 'İçeriğinizin kaç kez DM ile paylaşıldığını veya story\'ye eklendiğini gösterir. Viral potansiyelin en güçlü göstergesidir. Her paylaşım organik takipçi kazanma şansı demektir.',
    category: 'Metrikler',
    example: 'Yüksek paylaşım alan içerikler genelde relatable, komik veya çok faydalı olanlardır',
  },
  {
    term: 'Watch Time',
    simpleExplanation: 'Video içeriklerinin ortalama izlenme süresini gösterir. Reels için en kritik metriktir. %50+ izlenme oranı (15sn videoyu 7+ sn izleme) algoritma için pozitif sinyal. Düşük watch time = hook\'unuz zayıf veya içerik sıkıcı.',
    category: 'Metrikler',
    example: '30 saniyelik videoda ortalama 20sn izlenme = %66 retention (harika!)',
  },
  {
    term: 'Completion Rate',
    simpleExplanation: 'Videoyu sonuna kadar izleyenlerin oranı. %30+ completion rate iyi, %50+ mükemmeldir. Düşük oran videolarınızın çok uzun olduğunu veya ilgi kaybettirdiğini gösterir.',
    category: 'Metrikler',
  },
  
  // === CONTENT TERMS (İçerik Terimleri) ===
  {
    term: 'Hook',
    simpleExplanation: 'İçeriğin ilk 0.5-3 saniyesindeki dikkat yakalama anı. Scroll durduran, merak uyandıran açılış. Modern sosyal medyada hayati öneme sahiptir çünkü kullanıcı ilk 1 saniyede "izleyecek miyim?" kararını verir. Zayıf hook = içerik görünmez.',
    category: 'İçerik',
    example: '"Bu hatayı yapan herkes başarısız oluyor", "3 yılda 0\'dan 1M\'a nasıl çıktım?", "Kimse bunu söylemiyor ama..."',
  },
  {
    term: 'CTA (Call to Action)',
    simpleExplanation: 'Takipçiye ne yapması gerektiğini söyleyen net çağrı. Her içerik bir CTA içermelidir. Beğen, kaydet, yorum yaz, bio\'daki linke tıkla, takip et gibi. CTA olmadan etkileşim şansa kalır.',
    category: 'İçerik',
    example: 'Zayıf: "Ne düşünüyorsunuz?" / Güçlü: "Senin en büyük hatanı yorumlara yaz, birlikte çözelim!"',
  },
  {
    term: 'Content Pillar',
    simpleExplanation: 'Hesabınızın temel içerik kategorileri. 3-5 ana pillar belirlenmeli. Her pillar farklı bir amaca hizmet eder: Eğitim (değer), Eğlence (reach), İlham (bağ), Tanıtım (satış). Pillar belirsizliği takipçi kafası karıştırır.',
    category: 'İçerik',
    example: 'Fitness hesabı: 1) Antrenman teknikleri 2) Beslenme ipuçları 3) Motivasyon 4) Transformation hikayeleri',
  },
  {
    term: 'Reels',
    simpleExplanation: 'Instagram\'ın kısa video formatı (3-90 saniye). Algoritmada en güçlü reach potansiyeline sahip format. Trend ses kullanımı, hızlı kesimler ve güçlü hook\'lar başarı anahtarı. Keşfet sayfasında çıkma şansı en yüksek içerik türü.',
    category: 'İçerik',
    example: '15-30 saniyelik reels\'ler genelde en iyi performansı gösterir',
  },
  {
    term: 'Carousel',
    simpleExplanation: 'Birden fazla slayt içeren kaydırmalı gönderi (max 20 slayt). Eğitim içeriği için en ideal format. Yüksek save rate ve dwell time sağlar. İlk slayt hook, son slayt CTA olmalı. Orta slaytlar değer sunmalı.',
    category: 'İçerik',
    example: '"5 Adımda Instagram Büyütme" gibi adım adım rehberler carousel için mükemmel',
  },
  {
    term: 'Story',
    simpleExplanation: '24 saat sonra kaybolan geçici içerik. Günlük bağlantı kurma ve "arkadaşlarınız" hissiyatı için kullanılır. Poll, soru, quiz gibi interaktif öğelerle etkileşimi artırın. Çok sık story atan hesaplar öne çıkar.',
    category: 'İçerik',
    example: 'Günde 5-10 story ideal. Sabah, öğlen, akşam dağılımı yapın.',
  },
  {
    term: 'UGC (User Generated Content)',
    simpleExplanation: 'Takipçileriniz tarafından oluşturulan içerik. Müşteri yorumları, kullanıcı fotoğrafları, testimonial\'lar. En güvenilir içerik türüdür çünkü gerçek kullanıcılardan gelir. Sosyal kanıt oluşturur.',
    category: 'İçerik',
  },
  {
    term: 'Evergreen Content',
    simpleExplanation: 'Zamanla değer kaybetmeyen, her zaman geçerli içerik. "Instagram algoritması nedir?" gibi sürekli aranan konular. Uzun vadede organik trafik getirir. Her hesapta %30-40 evergreen içerik olmalı.',
    category: 'İçerik',
  },
  
  // === AUDIENCE TERMS (Kitle Terimleri) ===
  {
    term: 'Persona',
    simpleExplanation: 'İdeal takipçinizin detaylı profili. Yaş, cinsiyet, meslek, gelir, hobiler, sorunlar, hayaller dahil. Persona belirsiz = içerik belirsiz = büyüme yok. Tek bir kişiye konuşur gibi içerik üretin.',
    category: 'Kitle',
    example: '28 yaşında, İstanbul\'da yaşayan, e-ticaret yapan, ayda 15-30K kazanan, iş-yaşam dengesi arayan kadın girişimci',
  },
  {
    term: 'Pain Point',
    simpleExplanation: 'Takipçilerinizin yaşadığı sorunlar, acılar ve hayal kırıklıkları. İçerik stratejinizin temeli olmalı. Her içerik bir pain point\'e çözüm sunmalı veya ona değinmeli. Pain point anlamayan hesap büyüyemez.',
    category: 'Kitle',
    example: '"Takipçi kazanamıyorum", "Satış yapamıyorum", "Ne içerik üreteceğimi bilmiyorum", "Algoritmayı anlayamıyorum"',
  },
  {
    term: 'Bot Score',
    simpleExplanation: 'Takipçilerinizin yüzde kaçının sahte, bot veya inaktif hesap olduğunun tahmini. Yüksek bot score = düşük engagement, kötü algoritma sinyali, güvenilirlik kaybı. %5-10 normal, %20+ tehlikeli.',
    category: 'Kitle',
    example: 'Sahte takipçi satın almak bot score\'u yükseltir ve uzun vadede hesaba zarar verir',
  },
  {
    term: 'Follower Segmentation',
    simpleExplanation: 'Takipçilerin aktiflik ve değere göre gruplandırılması. Süper fanlar (%5), aktif takipçiler (%20), pasif takipçiler (%40), hayalet takipçiler (%25), bot/spam (%10). Her segmente farklı strateji gerekir.',
    category: 'Kitle',
  },
  {
    term: 'Follower/Following Ratio',
    simpleExplanation: 'Takipçi sayınızın takip ettiğiniz kişi sayısına oranı. Yüksek oran = otorite ve talep göstergesi. Takipçi > Takip eden iyi. 1000 takipçi / 100 takip = 10:1 oran (güçlü profil).',
    category: 'Kitle',
    example: '10K takipçi, 5K takip = 2:1 (normal). 10K takipçi, 500 takip = 20:1 (çok iyi)',
  },
  {
    term: 'Super Fans',
    simpleExplanation: 'Her içeriğinize tepki veren, savunuculuk yapan, ürünlerinizi satın alan en değerli %1-5 takipçi kitlesi. Bu kitleyi tanıyın, özel muamele gösterin, onlarla ilişki kurun.',
    category: 'Kitle',
  },
  
  // === GROWTH TERMS (Büyüme Terimleri) ===
  {
    term: 'Viral Loop',
    simpleExplanation: 'İçeriğin kendi kendini yayan döngü mekanizması. Paylaşım → yeni izleyici → yeni takipçi → yeni paylaşım. Viral içerik bu döngüyü tetikler. Paylaşılabilir ve relatable içerik üretin.',
    category: 'Büyüme',
    example: 'Tartışmalı görüşler, sektör sırları, herkesin yaşadığı ama konuşmadığı durumlar viral loop başlatır',
  },
  {
    term: 'Growth Rate',
    simpleExplanation: 'Belirli bir dönemde takipçi sayısının yüzde kaç arttığı. Haftalık %1-3 büyüme iyi, %5+ mükemmel. Negatif growth ciddi sorun işareti. Sektör ortalamasıyla karşılaştırın.',
    category: 'Büyüme',
    example: 'Ocak başı: 10.000 takipçi, Ocak sonu: 10.500 takipçi = %5 aylık growth rate',
  },
  {
    term: 'Competitor Gap',
    simpleExplanation: 'Rakiplerinizin yaptığı ama sizin yapmadığınız şeyler. Fırsat alanlarını gösterir. Rakip analizi yaparak gap\'leri bulun ve doldurun. Onların zayıf olduğu yerde güçlü olun.',
    category: 'Büyüme',
  },
  {
    term: 'Niche',
    simpleExplanation: 'Odaklandığınız spesifik alan/konu. Niche ne kadar dar olursa rekabet o kadar az, otorite o kadar kolay. "Fitness" değil "40+ kadınlar için evde pilates" gibi spesifik olun.',
    category: 'Büyüme',
    example: 'Genel: Yemek tarifleri / Niche: 15 dakikada hazırlanan vegan Türk mutfağı tarifleri',
  },
  {
    term: 'Authority Building',
    simpleExplanation: 'Alanınızda uzman/lider olarak algılanma süreci. Tutarlı değer paylaşımı, sosyal kanıt, medya görünürlüğü ve topluluk oluşturma ile sağlanır. Otorite = güven = satış.',
    category: 'Büyüme',
  },
  {
    term: 'Collaboration',
    simpleExplanation: 'Benzer niş\'teki diğer hesaplarla ortak içerik üretimi. Takipçi havuzlarını paylaşarak çapraz büyüme sağlar. Win-win işbirlikleri arayın. Canlı yayınlar, ortak carousel\'ler, takeover\'lar.',
    category: 'Büyüme',
  },
  
  // === VISUAL TERMS (Görsel Terimler) ===
  {
    term: 'Color Palette',
    simpleExplanation: 'Hesabınızın tüm görsellerinde tutarlı kullandığınız 3-5 ana renk seti. Marka tanınırlığı oluşturur. Feed\'i görsel olarak uyumlu hale getirir. Renk psikolojisini öğrenin.',
    category: 'Görsel',
    example: 'Sıcak tonlar (turuncu, sarı) = enerji, neşe. Soğuk tonlar (mavi, yeşil) = güven, huzur.',
  },
  {
    term: 'Grid Aesthetic',
    simpleExplanation: 'Profil sayfanızdaki 9-12 gönderinin bir arada nasıl göründüğü. İlk izlenimi belirler. Renk tutarlılığı, şablon kullanımı ve görsel ritim önemli. Kaotik grid = amatör algısı.',
    category: 'Görsel',
  },
  {
    term: 'Thumbnail',
    simpleExplanation: 'Video içeriğinin kapak görseli. Tıklama oranını direkt etkiler. Merak uyandırıcı, okunabilir metin içeren, yüz ifadesi gösteren thumbnail\'lar daha iyi performans gösterir.',
    category: 'Görsel',
    example: 'Şaşkın yüz ifadesi, büyük metin, kontrastlı renkler = yüksek CTR',
  },
  {
    term: 'Visual Consistency',
    simpleExplanation: 'Tüm içeriklerde benzer font, renk, filter ve stil kullanımı. Marka kimliğinin temel taşı. Tutarsız görsel = güvenilmez algısı. Şablon kullanımı tutarlılığı kolaylaştırır.',
    category: 'Görsel',
  },
  {
    term: 'Whitespace',
    simpleExplanation: 'Görsellerdeki boş alan kullanımı. Daha az bazen daha fazladır. Kalabalık tasarımlar yorucu, temiz tasarımlar profesyonel görünür. Metin ve görsel arasında nefes alanı bırakın.',
    category: 'Görsel',
  },
  
  // === ALGORITHM TERMS (Algoritma Terimleri) ===
  {
    term: 'Algorithm',
    simpleExplanation: 'Instagram\'ın hangi içeriği kime, ne zaman göstereceğine karar veren yapay zeka sistemi. Etkileşim, ilgi, yenilik, ilişki gibi yüzlerce sinyali değerlendirir. Algoritmayı anlamak büyümenin anahtarıdır.',
    category: 'Platform',
    example: 'Takipçiniz içeriğinizi beğenirse, algoritma ona daha çok içeriğinizi gösterir',
  },
  {
    term: 'Shadowban',
    simpleExplanation: 'Hesabın gizlice erişiminin kısıtlanması, içeriklerin keşfet ve hashtag\'lerde görünmemesi. Spam davranışı, yasaklı hashtag kullanımı, çok hızlı takip/bırakma gibi sebeplerden olur. Ciddi büyüme engelidir.',
    category: 'Platform',
    example: 'Engagement aniden düştüyse ve keşfette görünmüyorsanız shadowban olabilirsiniz',
  },
  {
    term: 'Hashtag Strategy',
    simpleExplanation: 'Doğru hashtag kombinasyonunu seçme sanatı. Çok popüler (10M+) hashtag\'lerde kaybolursunuz, çok niş olanlarda kimse aramaz. Karışık kullanın: %30 büyük, %40 orta, %30 niş.',
    category: 'Platform',
    example: '#fitness (500M - çok büyük) + #evdeantrenman (1M - orta) + #istanbulfitness (10K - niş)',
  },
  {
    term: 'Peak Hours',
    simpleExplanation: 'Takipçilerinizin en aktif olduğu saatler. Bu saatlerde paylaşım yapın. Instagram Insights\'tan görebilirsiniz. Genelde sabah 7-9, öğle 12-14, akşam 19-22 aktif dönemlerdir.',
    category: 'Platform',
  },
  {
    term: 'Dwell Time',
    simpleExplanation: 'Kullanıcıların içeriğinizde ne kadar süre geçirdiği. Carousel\'lerde kaydırma, video\'larda izleme, caption\'da okuma süresi. Uzun dwell time = algoritma sizi sever = daha fazla reach.',
    category: 'Platform',
  },
  {
    term: 'Explore Page',
    simpleExplanation: 'Instagram\'ın kişiselleştirilmiş keşfet sayfası. Burada çıkmak organik büyümenin en güçlü yolu. Yüksek engagement, hızlı etkileşim ve trend konular explore\'a çıkma şansını artırır.',
    category: 'Platform',
  },
  
  // === BUSINESS TERMS (İş Terimleri) ===
  {
    term: 'Conversion Rate',
    simpleExplanation: 'Takipçilerin istenen aksiyonu tamamlama oranı (satın alma, kayıt, tıklama). 100 tıklamadan 3 satış = %3 conversion rate. E-ticaret için %1-3 normal, %5+ mükemmel.',
    category: 'İş',
    example: '1000 profil ziyareti, 50 link tıklaması, 5 satış = %0.5 overall conversion',
  },
  {
    term: 'Monetization',
    simpleExplanation: 'Sosyal medya varlığınızdan gelir elde etme yöntemleri. Sponsorluk, affiliate marketing, kendi ürünleri, danışmanlık, eğitim satışı gibi. Çeşitli gelir kaynakları oluşturun.',
    category: 'İş',
    example: '10K+ takipçiyle mikro-influencer sponsorlukları almaya başlayabilirsiniz',
  },
  {
    term: 'ROI (Return on Investment)',
    simpleExplanation: 'Yatırımınızın geri dönüşü. Harcadığınız zaman/para karşılığında ne kazandınız? Pozitif ROI = karlı strateji. Negatif ROI = strateji değişikliği gerekli.',
    category: 'İş',
  },
  {
    term: 'Sales Funnel',
    simpleExplanation: 'Yabancıları müşteriye dönüştüren adım adım süreç. Farkındalık → İlgi → Değerlendirme → Satın alma. Her adımda içerik ve CTA farklı olmalı. Instagram tüm funnel\'ı destekler.',
    category: 'İş',
    example: 'Reels (farkındalık) → Carousel (eğitim) → Story (güven) → DM (satış)',
  },
  {
    term: 'Social Proof',
    simpleExplanation: 'Başkalarının onayını göstererek güven oluşturma. Müşteri yorumları, rakamlar (10K+ müşteri), medya logoları, before/after görselleri. İnsanlar kalabalığı takip eder.',
    category: 'İş',
  },
  {
    term: 'Lead Generation',
    simpleExplanation: 'Potansiyel müşteri bilgisi toplama. E-posta, telefon, DM gibi iletişim kanalları açma. Ücretsiz değer karşılığı bilgi alın (lead magnet). Sonra bu listeye satış yapın.',
    category: 'İş',
  },
  {
    term: 'Affiliate Marketing',
    simpleExplanation: 'Başka markaların ürünlerini tanıtıp satış başına komisyon kazanma. Kendi ürününüz olmadan gelir elde etmenin en kolay yolu. Güvendiğiniz ürünleri önerin.',
    category: 'İş',
  },
  
  // === ANALYTICS TERMS (Analitik Terimleri) ===
  {
    term: 'KPI (Key Performance Indicator)',
    simpleExplanation: 'Başarıyı ölçtüğünüz temel metrikler. Her hesabın KPI\'ları farklı olabilir: büyüme için takipçi artışı, satış için conversion rate, marka bilinirliği için reach. 3-5 KPI belirleyin ve takip edin.',
    category: 'Analitik',
  },
  {
    term: 'Benchmark',
    simpleExplanation: 'Performansınızı karşılaştırdığınız referans değerler. Sektör ortalaması, rakip performansı veya kendi geçmiş performansınız. Benchmark olmadan "iyi miyim?" sorusuna cevap veremezsiniz.',
    category: 'Analitik',
  },
  {
    term: 'A/B Testing',
    simpleExplanation: 'İki farklı versiyonu test ederek hangisinin daha iyi performans gösterdiğini bulma. Farklı hook\'lar, thumbnail\'lar, CTA\'lar deneyin. Veriye dayalı karar alın, tahmin yapmayın.',
    category: 'Analitik',
    example: 'Aynı içeriği farklı saatlerde paylaşarak en iyi zamanı bulabilirsiniz',
  },
  {
    term: 'Attribution',
    simpleExplanation: 'Bir sonucun (satış, kayıt) hangi içerik veya kampanyadan geldiğini takip etme. UTM parametreleri, özel linkler, anketler kullanarak attribution yapın. Neyin işe yaradığını bilin.',
    category: 'Analitik',
  },
];

interface JargonGlossaryProps {
  additionalTerms?: GlossaryTerm[];
  highlightedTerms?: string[];
  compact?: boolean;
}

const JargonGlossary: React.FC<JargonGlossaryProps> = ({
  additionalTerms = [],
  highlightedTerms = [],
  compact = false,
}) => {
  const { t, locale } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(!compact);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const allTerms = [...defaultGlossaryTerms, ...additionalTerms];
  
  // Get unique categories
  const categories = Array.from(new Set(allTerms.map(t => t.category).filter(Boolean)));
  
  // Filter terms
  const filteredTerms = allTerms.filter(term => {
    const matchesSearch = searchQuery === '' || 
      term.term.toLowerCase().includes(searchQuery.toLowerCase()) ||
      term.simpleExplanation.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = !selectedCategory || term.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Sort highlighted terms first
  const sortedTerms = [...filteredTerms].sort((a, b) => {
    const aHighlighted = highlightedTerms.includes(a.term);
    const bHighlighted = highlightedTerms.includes(b.term);
    if (aHighlighted && !bHighlighted) return -1;
    if (!aHighlighted && bHighlighted) return 1;
    return a.term.localeCompare(b.term);
  });

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-full bg-purple-100">
            <BookOpenIcon className="h-5 w-5 text-purple-600" />
          </div>
          <div className="text-left">
            <h3 className="text-lg font-semibold text-slate-900">📖 {t('glossary.title')}</h3>
            <p className="text-sm text-slate-500">
              {locale === 'en' ? 'Simple explanations of technical terms' : 'Teknik terimlerin basit açıklamaları'}
            </p>
          </div>
        </div>
        {isExpanded ? (
          <ChevronUpIcon className="w-5 h-5 text-slate-400" />
        ) : (
          <ChevronDownIcon className="w-5 h-5 text-slate-400" />
        )}
      </button>

      {/* Content */}
      {isExpanded && (
        <div className="px-6 pb-6 space-y-4">
          {/* Search and Filter */}
          <div className="flex flex-col sm:flex-row gap-3">
            {/* Search */}
            <div className="relative flex-1">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                placeholder={t('glossary.searchTerms')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 bg-slate-50 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            
            {/* Category Filter */}
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setSelectedCategory(null)}
                className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
                  !selectedCategory 
                    ? 'bg-primary-500 text-white' 
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {t('glossary.allCategories')}
              </button>
              {categories.map(category => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category || null)}
                  className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
                    selectedCategory === category 
                      ? 'bg-primary-500 text-white' 
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Terms List */}
          <div className="grid gap-3">
            {sortedTerms.map((term, idx) => (
              <div 
                key={idx}
                className={`p-4 rounded-xl border transition-colors ${
                  highlightedTerms.includes(term.term)
                    ? 'border-primary-200 bg-primary-50/50'
                    : 'border-slate-200 bg-slate-50/50 hover:bg-slate-50'
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h4 className="font-semibold text-slate-900">{term.term}</h4>
                      {term.category && (
                        <span className="px-2 py-0.5 rounded-full text-xs bg-slate-200 text-slate-600">
                          {term.category}
                        </span>
                      )}
                      {highlightedTerms.includes(term.term) && (
                        <span className="px-2 py-0.5 rounded-full text-xs bg-primary-200 text-primary-700">
                          {locale === 'en' ? 'In report' : 'Raporda geçiyor'}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-slate-600 mt-1">{term.simpleExplanation}</p>
                    {term.example && (
                      <p className="text-xs text-slate-500 mt-2 italic">
                        💡 {t('glossary.example')}: {term.example}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {sortedTerms.length === 0 && (
            <p className="text-center text-slate-500 py-4">{t('glossary.noTermsFound')}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default JargonGlossary;

// Helper to extract technical terms from text
export function extractTechnicalTerms(text: string): string[] {
  const knownTerms = defaultGlossaryTerms.map(t => t.term.toLowerCase());
  const words = text.toLowerCase().split(/\s+/);
  
  return knownTerms.filter(term => 
    words.some(word => word.includes(term.toLowerCase().split(' ')[0]))
  );
}
