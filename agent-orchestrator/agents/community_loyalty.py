"""Community Loyalty Architect Agent - PhD Level Implementation.

Bu ajan topluluk psikolojisi, bağlılık metrikleri ve UGC/ambassador stratejilerine
odaklanır. Loyalty ve community health skorlarını hesaplar, sentiment ve churn
risklerini değerlendirir, ritüeller ile yanıt stratejileri önerir.
"""

from typing import Any, Dict, List, Optional, Tuple

from .base_agent import BaseAgent


class CommunityLoyaltyAgent(BaseAgent):
	"""
	Community Loyalty Architect Agent - PhD Level

	Uzmanlık Alanları:
	- Topluluk psikolojisi ve bağlılık katmanları
	- Engagement derinlik analizi ve yorum kalitesi
	- Sentiment, churn ve loyalty index hesaplamaları
	- Superfan tespiti, UGC ve ambassador programları
	- Ritual tasarımı, yanıt ve re-engagement stratejileri

	Metrikler:
	- Community Health Score (0-100)
	- Loyalty Index (0-100)
	- Engagement Quality Score (0-100)
	- Sentiment Score (0-100)
	- Superfan Percentage (%)
	- Response Rate Recommendation (%)
	- Avg Engagement Depth (surface-light-medium-deep-advocacy)
	"""

	def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
		super().__init__(gemini_client, generation_config, model_name)
		self.name = "Community Loyalty Architect"
		self.role = "Community Health & Loyalty Strategist"
		self.specialty = (
			"Community psychology, loyalty engineering, superfans, UGC, ambassador programs, "
			"ritual design, response strategy"
		)

		# Initialize knowledge bases
		self._init_community_layers()
		self._init_loyalty_psychology()
		self._init_health_indicators()
		self._init_engagement_depth()
		self._init_comment_framework()
		self._init_sentiment_framework()
		self._init_superfan_framework()
		self._init_loyalty_index_framework()
		self._init_churn_model()
		self._init_engagement_strategies()
		self._init_rituals()
		self._init_response_strategy()
		self._init_ugc_ambassador()
		self._init_scoring_models()

	# ---------------------- Knowledge Bases ----------------------
	def _init_community_layers(self) -> None:
		self.community_layers = {
			"superfans": {"share": (0.01, 0.03), "value": "advocates", "multiplier": 40},
			"active_engagers": {"share": (0.05, 0.10), "value": "algorithm support", "multiplier": 15},
			"regular": {"share": (0.15, 0.25), "value": "steady engagement", "multiplier": 5},
			"passive": {"share": (0.40, 0.50), "value": "reach padding", "multiplier": 1},
			"ghost": {"share": (0.20, 0.30), "value": "drag", "multiplier": -1},
		}

		self.community_value = {
			"superfan_value_x": (10, 50),
			"active_engager_value_x": (3, 5),
			"behaviors": {
				"superfans": ["advocacy", "ugc", "defense", "referral"],
				"active_engagers": ["regular_comments", "shares", "saves"],
			},
		}

		self.community_development = ["forming", "storming", "norming", "performing", "transforming"]

	def _init_loyalty_psychology(self) -> None:
		self.loyalty_factors = {
			"emotional_connection": {"components": ["shared_values", "stories", "vulnerability", "authenticity"], "impact": 5},
			"value_delivery": {"components": ["quality", "problem_solving", "entertainment", "education"], "impact": 5},
			"recognition": {"components": ["reply", "feature", "shoutout", "exclusive_access"], "impact": 4},
			"belonging": {"components": ["identity", "inside_jokes", "language", "rituals"], "impact": 5},
			"reciprocity": {"components": ["give_before_ask", "respond", "value_exchange"], "impact": 4},
		}

		self.loyalty_levels = {
			1: "awareness",
			2: "interest",
			3: "engagement",
			4: "commitment",
			5: "advocacy",
		}

	def _init_health_indicators(self) -> None:
		self.health_positive = {
			"engagement_quality": ["meaningful_comments", "follower_discussion", "organic_shares"],
			"growth_patterns": ["steady_growth", "low_unfollow", "referral_traffic"],
			"sentiment_signals": ["positive_emojis", "supportive_comments", "defense"],
			"behavioral": ["notifications_on", "story_consistency", "dm_activity", "live_participation"],
		}

		self.health_negative = {
			"engagement_red_flags": ["emoji_only", "bot_generic", "declining_trend", "negative_rise"],
			"growth_red_flags": ["high_unfollow", "follower_engagement_gap", "spike_and_drop", "ghost_rise"],
			"sentiment_red_flags": ["criticism_rise", "trolls", "silent_churn", "negative_mentions"],
		}

	def _init_engagement_depth(self) -> None:
		self.depth_levels = {
			1: {"name": "surface", "value": 1, "examples": ["like", "emoji_comment"]},
			2: {"name": "light", "value": 2, "examples": ["short_comment", "story_reaction", "quick_save"]},
			3: {"name": "medium", "value": 5, "examples": ["meaningful_comment", "story_reply", "share_close_friends"]},
			4: {"name": "deep", "value": 10, "examples": ["long_comment", "dm_conversation", "public_share", "tag_friends"]},
			5: {"name": "advocacy", "value": 25, "examples": ["ugc", "testimonial", "defense", "referral"]},
		}

		self.depth_distribution_benchmark = {
			"surface": (0.60, 0.70),
			"light": (0.15, 0.25),
			"medium": (0.08, 0.12),
			"deep": (0.03, 0.05),
			"advocacy": (0.005, 0.02),
		}

	def _init_comment_framework(self) -> None:
		self.comment_categories = {
			"appreciation": {"sentiment": "positive", "value": "low_medium"},
			"question": {"sentiment": "neutral", "value": "high"},
			"story": {"sentiment": "positive", "value": "very_high"},
			"discussion": {"sentiment": "mixed", "value": "very_high"},
			"tagging": {"sentiment": "positive", "value": "very_high"},
			"spam": {"sentiment": "na", "value": "negative"},
		}

		self.comment_length_scores = [(2, 20), (10, 50), (30, 80), (999, 100)]
		self.comment_relevance_scores = {
			"off_topic": 10,
			"generic": 40,
			"related": 70,
			"highly_relevant": 100,
		}

	def _init_sentiment_framework(self) -> None:
		self.sentiment_categories = {
			"very_positive": {"score": (90, 100), "weight": 1.0},
			"positive": {"score": (70, 89), "weight": 1.0},
			"neutral": {"score": (40, 69), "weight": 0.8},
			"negative": {"score": (20, 39), "weight": 1.2},
			"very_negative": {"score": (0, 19), "weight": 1.5},
		}

		self.sentiment_benchmarks = {
			"excellent": (80, 100),
			"good": (70, 79),
			"average": (60, 69),
			"concerning": (50, 59),
			"critical": (0, 49),
		}

	def _init_superfan_framework(self) -> None:
		self.superfan_criteria = {
			"frequency": {"threshold": 0.80},
			"depth": {"threshold": 3},
			"advocacy": {"threshold": 2},
			"tenure_months": {"threshold": 6},
			"ugc": {"threshold": 1},
		}

		self.superfan_classification = {
			"ultra_superfan": (90, 100),
			"superfan": (75, 89),
			"potential": (60, 74),
			"active_engager": (45, 59),
			"regular": (0, 44),
		}

		self.superfan_segment_benchmarks = {
			"lt_10k": {"superfan": (0.03, 0.05), "active": (0.15, 0.25)},
			"10k_50k": {"superfan": (0.02, 0.04), "active": (0.10, 0.20)},
			"50k_100k": {"superfan": (0.01, 0.03), "active": (0.08, 0.15)},
			"100k_500k": {"superfan": (0.005, 0.02), "active": (0.05, 0.12)},
			"500k_plus": {"superfan": (0.003, 0.01), "active": (0.03, 0.08)},
		}

	def _init_loyalty_index_framework(self) -> None:
		self.loyalty_components = {
			"retention": 0.30,
			"engagement_quality": 0.25,
			"advocacy": 0.20,
			"responsiveness": 0.15,
			"tenure": 0.10,
		}

		self.loyalty_benchmarks = {
			"exceptional": (85, 100),
			"strong": (70, 84),
			"moderate": (55, 69),
			"weak": (40, 54),
			"crisis": (0, 39),
		}

	def _init_churn_model(self) -> None:
		self.churn_base_risk = {
			"ghost": 0.40,
			"passive": 0.15,
			"regular": 0.08,
			"active": 0.03,
			"superfan": 0.01,
		}

		self.churn_signals = {
			"high": {"multiplier": 3.0, "signals": ["engagement_drop_50", "no_interaction_14d", "story_stop", "negative_history"]},
			"medium": {"multiplier": 2.0, "signals": ["engagement_drop_25", "reduced_frequency", "skip_pattern", "generic_only"]},
			"low": {"multiplier": 1.2, "signals": ["slight_decrease", "seasonal", "format_shift"]},
		}

	def _init_engagement_strategies(self) -> None:
		self.engagement_strategies = {
			"tier1": [
				{"strategy": "daily_question_sticker", "impact": (0.20, 0.40), "effort": "low"},
				{"strategy": "poll_quiz_weekly", "impact": (0.30, 0.50), "effort": "low"},
				{"strategy": "caption_question", "impact": (0.15, 0.25), "effort": "low"},
				{"strategy": "reply_all_comments", "impact": (0.25, 0.40), "effort": "medium"},
			],
			"tier2": [
				{"strategy": "user_spotlight", "impact": (0.20, 0.30), "effort": "medium"},
				{"strategy": "behind_the_scenes", "impact": (0.25, 0.25), "effort": "medium"},
				{"strategy": "live_qa", "impact": (0.40, 0.40), "effort": "medium"},
				{"strategy": "comment_challenge", "impact": (0.50, 0.50), "effort": "medium"},
			],
			"tier3": [
				{"strategy": "ambassador_program", "impact": (1.0, 1.0), "effort": "high"},
				{"strategy": "exclusive_community", "impact": (0.60, 0.60), "effort": "high"},
				{"strategy": "co_creation", "impact": (0.35, 0.35), "effort": "high"},
			],
		}

	def _init_rituals(self) -> None:
		self.rituals = {
			"daily": [
				{"name": "morning_checkin", "window": "07:00-09:00", "purpose": "habit"},
				{"name": "daily_tip", "window": "consistent", "purpose": "value"},
				{"name": "evening_engagement", "window": "19:00-21:00", "purpose": "bonding"},
			],
			"weekly": [
				{"name": "themed_day", "purpose": "anticipation"},
				{"name": "weekly_recap", "purpose": "value_summary"},
				{"name": "community_spotlight", "purpose": "recognition"},
				{"name": "qa_session", "purpose": "direct_engagement"},
			],
			"monthly": [
				{"name": "challenge", "duration_days": (7, 30)},
				{"name": "giveaway", "purpose": "growth_engagement"},
				{"name": "milestone_celebration", "purpose": "shared_achievement"},
				{"name": "feedback_session", "purpose": "community_input"},
			],
		}

	def _init_response_strategy(self) -> None:
		self.response_targets = {
			"comment": {"ideal": 1, "acceptable": 4},
			"dm": {"ideal": 4, "acceptable": 24},
			"story": {"ideal": 2, "acceptable": 4},
			"mention": {"ideal": 6, "acceptable": 12},
			"crisis": {"ideal": 0.5, "acceptable": 0.5},
		}

		self.response_priority_matrix = {
			"question": {"priority": "high", "time_hours": 1},
			"complaint": {"priority": "urgent", "time_hours": 0.5},
			"praise": {"priority": "medium", "time_hours": 4},
			"story_share": {"priority": "high", "time_hours": 2},
			"tag": {"priority": "medium", "time_hours": 6},
			"generic": {"priority": "low", "time_hours": 24},
			"spam": {"priority": "none", "time_hours": None},
		}

	def _init_ugc_ambassador(self) -> None:
		self.ugc_types = ["testimonial", "recreation", "mention", "fan_content"]
		self.ugc_tactics = ["branded_hashtag", "challenge", "template_sharing", "feature_promise"]
		self.ugc_do = ["credit", "permission", "add_value", "thank", "highlight"]
		self.ugc_dont = ["no_credit", "no_permission", "over_repost", "ignore_low_quality", "no_engage"]

		self.ambassador_tiers = {
			1: {"name": "community_member", "benefits": ["recognition", "early_access"], "responsibility": "regular_engagement"},
			2: {"name": "brand_friend", "benefits": ["exclusive_content", "shoutouts"], "responsibility": "monthly_ugc"},
			3: {"name": "ambassador", "benefits": ["products", "affiliate", "features"], "responsibility": "weekly_promotion"},
			4: {"name": "vip_ambassador", "benefits": ["paid_collab", "events", "strategy_input"], "responsibility": "campaign_participation"},
		}

		self.ambassador_selection = {
			"quantitative": {"engagement_consistency": 0.80, "content_quality": "high", "audience_alignment": 0.70, "duration_months": 6},
			"qualitative": ["values", "communication", "creativity", "reliability", "authenticity"],
		}

	def _init_scoring_models(self) -> None:
		self.community_health_weights = {
			"engagement_quality": 0.30,
			"sentiment": 0.25,
			"growth_health": 0.20,
			"retention": 0.25,
		}

		self.engagement_quality_weights = {
			"comment_quality": 0.35,
			"engagement_diversity": 0.25,
			"authenticity": 0.25,
			"depth_distribution": 0.15,
		}

		self.sentiment_weights = {
			"very_positive": 1.0,
			"positive": 1.0,
			"neutral": 0.8,
			"negative": 1.2,
			"very_negative": 1.5,
		}

		self.response_improvement_targets = [
			(30, 30, "critical"),
			(50, 20, "high"),
			(70, 15, "medium"),
			(90, 10, "low"),
		]

	# ---------------------- Calculations ----------------------
	def calculate_engagement_depth_average(self, depth_counts: Dict[str, int]) -> float:
		total = sum(depth_counts.values()) or 1
		score_sum = 0.0
		for level, count in depth_counts.items():
			value = 0
			for lvl, meta in self.depth_levels.items():
				if meta["name"] == level:
					value = meta["value"]
					break
			score_sum += count * value
		return score_sum / total

	def calculate_depth_assessment(self, depth_distribution: Dict[str, float]) -> str:
		deviations = []
		for level, rng in self.depth_distribution_benchmark.items():
			observed = depth_distribution.get(level, 0)
			low, high = rng
			if observed < low * 0.8:
				deviations.append("too_low")
			elif observed > high * 1.2:
				deviations.append("too_high")
		return "balanced" if not deviations else "unbalanced"

	def calculate_comment_quality_score(
		self, length_score: float, relevance_score: float, engagement_potential: float, authenticity_score: float
	) -> float:
		return (
			length_score * 0.20
			+ relevance_score * 0.30
			+ engagement_potential * 0.25
			+ authenticity_score * 0.25
		)

	def calculate_sentiment_score(self, distribution: Dict[str, float], trend: Optional[str] = None, advocacy_bonus: bool = False) -> float:
		numerator = 0.0
		weight_sum = 0.0
		for cat, pct in distribution.items():
			weight = self.sentiment_weights.get(cat, 1.0)
			score_high = self.sentiment_categories.get(cat, {}).get("score", (50, 50))[1]
			numerator += pct * score_high * weight
			weight_sum += weight

		score = numerator / (weight_sum or 1)
		if trend == "improving":
			score += 5
		elif trend == "declining":
			score -= 5
		if advocacy_bonus:
			score += 5
		return max(0, min(100, score))

	def calculate_loyalty_index(
		self,
		retention: float,
		engagement_quality: float,
		advocacy: float,
		responsiveness: float,
		tenure: float,
	) -> float:
		weights = self.loyalty_components
		score = (
			retention * weights["retention"]
			+ engagement_quality * weights["engagement_quality"]
			+ advocacy * weights["advocacy"]
			+ responsiveness * weights["responsiveness"]
			+ tenure * weights["tenure"]
		)
		return max(0, min(100, score))

	def calculate_community_health(
		self, engagement_quality: float, sentiment: float, growth_health: float, retention: float
	) -> float:
		w = self.community_health_weights
		score = (
			engagement_quality * w["engagement_quality"]
			+ sentiment * w["sentiment"]
			+ growth_health * w["growth_health"]
			+ retention * w["retention"]
		)
		return max(0, min(100, score))

	def calculate_engagement_quality_score(
		self, comment_quality: float, engagement_diversity: float, authenticity: float, depth_distribution_score: float
	) -> float:
		w = self.engagement_quality_weights
		score = (
			comment_quality * w["comment_quality"]
			+ engagement_diversity * w["engagement_diversity"]
			+ authenticity * w["authenticity"]
			+ depth_distribution_score * w["depth_distribution"]
		)
		return max(0, min(100, score))

	def calculate_depth_distribution_score(self, depth_distribution: Dict[str, float]) -> float:
		score = 0.0
		for level, rng in self.depth_distribution_benchmark.items():
			observed = depth_distribution.get(level, 0)
			low, high = rng
			if low <= observed <= high:
				score += 25
			elif observed > high * 1.5:
				score -= 10
			else:
				score += 10 * (observed / low) if low else 0
		return max(0, min(100, score))

	def calculate_sentiment_classification(self, score: float) -> str:
		for label, (low, high) in self.sentiment_benchmarks.items():
			if low <= score <= high:
				return label
		return "critical"

	def calculate_superfan_percentage(self, identified: int, total_followers: int) -> float:
		if total_followers <= 0:
			return 0.0
		return (identified / total_followers) * 100

	def recommend_response_rate(self, current_rate: float, follower_count: int) -> float:
		target_add = 0
		for upper, delta, _ in self.response_improvement_targets:
			if current_rate < upper:
				target_add = delta
				break

		size_target = 90 if follower_count < 10_000 else 70 if follower_count < 50_000 else 50 if follower_count < 100_000 else 40
		recommended = min(100.0, max(size_target, current_rate + target_add))
		return recommended

	def calculate_churn_risk(self, segment: str, signal_strengths: List[str]) -> float:
		base = self.churn_base_risk.get(segment, 0.08)
		risk = base
		for strength, data in self.churn_signals.items():
			if any(sig in signal_strengths for sig in data["signals"]):
				risk *= data["multiplier"]
		return min(1.0, risk)

	def classify_loyalty(self, score: float) -> str:
		for label, (low, high) in self.loyalty_benchmarks.items():
			if low <= score <= high:
				return label
		return "crisis"

	def detect_edge_case(self, account_data: Dict[str, Any]) -> str:
		followers = account_data.get("followers", 0) or 0
		recent_growth = account_data.get("recent_growth", 0)
		sentiment_spike = account_data.get("sentiment_spike", "none")
		suspected_pod = account_data.get("engagement_pod_suspected", False)
		niche_change = account_data.get("niche_change", False)
		b2b = account_data.get("is_b2b", False)
		celebrity = account_data.get("is_celebrity", False)
		seasonal = account_data.get("is_seasonal", False)

		if followers < 1000:
			return "new_account"
		if recent_growth and recent_growth > 0.5:
			return "post_viral"
		if sentiment_spike == "negative":
			return "crisis"
		if suspected_pod:
			return "engagement_pod"
		if niche_change:
			return "niche_change"
		if b2b:
			return "b2b"
		if celebrity:
			return "celebrity"
		if seasonal:
			return "seasonal"
		return "none"

	# ---------------------- Prompts ----------------------
	def get_system_prompt(self) -> str:
		return """Sen Community Loyalty Architect Agent'sın - PhD seviyesinde topluluk psikolojisi ve bağlılık stratejisi uzmanı.

🔴 DİL KURALI: TÜM ANALİZ VE ÖNERİLER TÜRKÇE OLMALIDIR 🔴

UZMANLIK ALANLARIN:
- Topluluk psikolojisi ve katman dinamikleri
- Engagement derinlik analizi (surface → advocacy)
- Sentiment analizi ve trend tespiti
- Churn risk modelleme ve önleme
- Superfan tespiti ve ambassador program tasarımı
- UGC aktivasyonu ve topluluk ritüelleri
- Response stratejisi optimizasyonu

ANALİZ METODOLOJİN:
1. Community Health Score = (Engagement_Quality × 0.30) + (Sentiment × 0.25) + (Growth_Health × 0.20) + (Retention × 0.25)
2. Loyalty Index = (Retention × 0.30) + (Engagement_Quality × 0.25) + (Advocacy × 0.20) + (Responsiveness × 0.15) + (Tenure × 0.10)
3. Sentiment Score = Ağırlıklı ortalama (very_positive=1.0, positive=1.0, neutral=0.8, negative=1.2, very_negative=1.5)
4. Superfan % = (Tespit edilen superfan sayısı / Toplam takipçi) × 100

BENCHMARKS:
- Superfan oranı: <10K: %3-5, 10K-50K: %2-4, 50K-100K: %1-3, 100K-500K: %0.5-2, 500K+: %0.3-1
- Loyalty Index: Exceptional (85-100), Strong (70-84), Moderate (55-69), Weak (40-54), Crisis (<40)
- Sentiment: Excellent (80+), Good (70-79), Average (60-69), Concerning (50-59), Critical (<50)

=== BÖLÜM 9: 2026 TOPLULUK VE BAĞLILIK STRATEJİLERİ ===

📌 9.1 OTOMASYON ODAKLI TOPLULUK YÖNETİMİ (ManyChat Entegrasyonu)

A) COMMENT-TO-DM SİSTEMİ:
   - Amaç: Yorumlardaki ilgiyi DM'e çevirerek 1:1 ilişki kur
   - Tetikleyici Kelimeler: "link", "nasıl", "fiyat", "bilgi"
   - Otomasyon Akışı:
     1. Kullanıcı belirli kelime yorum yapar
     2. Sistem otomatik DM gönderir
     3. DM'de değer + CTA sunulur
   - ÖNEMLİ: Her Reel'de yorum tetikleyicisi olmalı
   - Örnek CTA: "Link için yoruma INFO yaz 📩"

B) FOLLOW-TO-DM SİSTEMİ:
   - Yeni takipçiye anında hoşgeldin DM'i
   - İçerik: Değer + En iyi içerikler + CTA
   - Amaç: İlk 24 saat içinde bağ kur

C) STORY REPLY OTOMASYONU:
   - Story'ye yanıt veren herkese otomatik DM
   - Amaç: Story engagement'ı konuşmaya çevir

📌 9.2 STD STRATEJİSİ - TOPLULUK AKTİVASYONU

STD = Silence → Tease → Deliver

48 SAAT SUSKUNLUK:
- Amaç: Algoritmanın seni "özlemesini" sağla
- Topluluk merakı ve beklentisi artar
- DM'ler düşer = DM açtığında algoritma ödüllendirir

TEK STORY (Tease):
- 48 saat sonra sadece 1 story at
- İçerik: Merak uyandıran, değer vaat eden
- Örnek: "Yarın büyük bir şey geliyor 👀"

DM TETİKLEYİCİ (Deliver):
- Story'de DM isteyen CTA
- "Merak edenler DM'den yazabilir"
- Sonuç: DM patlaması + reach patlaması

📌 9.3 TOPLULUK RİTÜELLERİ 2026

HAFTALIK RİTÜELLER:
- "Pazartesi Motivasyonu" - Haftaya başlangıç postu
- "Cuma Soru-Cevap" - Story'de topluluk katılımı
- "Pazar Özeti" - Haftanın en iyileri

AYLIK RİTÜELLER:
- "Ayın Süperstarı" - Topluluk üyesini öne çıkar
- "Behind the Scenes" - Kamera arkası içerik
- "Q&A Live" - Canlı yayın ile bağ kur

ENGAGEMENT TETİKLEYİCİLERİ:
- Her içerikte soru sor
- Poll/Quiz story'leri düzenli kullan
- "Kaydet" CTA'sı her içerikte olsun

📌 9.4 SUPERFAN GELİŞTİRME 2026

SUPERFAN YOLCULUĞU:
1. Takipçi → İlk yorum → İlk save → İlk share → DM etkileşimi → Superfan

SUPERFAN AKTİVASYON:
- İsimle hitap et (DM/yorum cevaplarında)
- Early access ver (yeni içerik önizlemesi)
- Exclusive içerik paylaş
- UGC fırsatı sun

AMBASSADOR PROGRAMI:
- Top %1 takipçiyi tespit et
- Özel Discord/Telegram grubu
- İçerik oluşturmaya davet et
- Referral sistemi kur

📌 9.5 YANIT STRATEJİSİ 2026

İLK 60 DAKİKA KURALI:
- Paylaşım sonrası ilk 60 dk kritik
- Her yoruma yanıt ver
- Uzun, değerli yanıtlar yaz
- Soru sorarak konuşma sürdür

YORUM KALİTESİ ÖNCELİKLENDİRME:
1. Soru içeren yorumlar (en yüksek öncelik)
2. Hikaye/deneyim paylaşan yorumlar
3. Etiketli yorumlar (@arkadas)
4. Uzun, detaylı yorumlar
5. Emoji-only yorumlar (düşük öncelik)

DM YÖNETİMİ:
- 24 saat içinde yanıt hedefi
- Sesli mesaj kullan (kişisellik)
- Video DM dene (güven inşası)

KRİTİK KURALLAR:
- Tüm skorları verilen formüllerle hesapla
- Edge case'leri tespit et ve yaklaşımı ayarla
- Çıktı MUTLAKA geçerli JSON formatında olmalı
- JSON dışında hiçbir metin yazma
- TÜM ÖNERİLER VE ANALİZLER TÜRKÇE OLMALIDIR"""

	def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
		return f"""Aşağıdaki Instagram hesap verilerini analiz et ve topluluk sağlığı değerlendirmesi yap.

=== HESAP VERİLERİ ===
{account_data}

=== ANALİZ GÖREVLERİ ===
1. TOPLULUK SAĞLIĞI: Community Health Score hesapla (formül: EQ×0.30 + Sentiment×0.25 + Growth×0.20 + Retention×0.25)
2. BAĞLILIK ANALİZİ: Loyalty Index hesapla, superfan yüzdesini belirle
3. ENGAGEMENT DERİNLİĞİ: Yorum kalitesi ve etkileşim derinliğini değerlendir
4. SENTIMENT: Duygu dağılımını analiz et, trend belirle
5. CHURN RİSKİ: Kayıp riski olan segmentleri tespit et
6. EDGE CASE: Özel durumları tespit et (yeni hesap, viral sonrası, kriz vb.)
7. STRATEJİLER: Engagement artırma, ritüel ve UGC önerileri üret

=== ÇIKTI FORMATI ===
Aşağıdaki JSON şemasına TAM UYUMLU yanıt ver. Ekstra metin veya açıklama YAZMA.

```json
{{
  "agent": "community_loyalty_architect",
  "analysis_timestamp": "ISO8601_formatında_tarih",
  "community_overview": {{
    "health_status": "healthy|at_risk|critical",
    "loyalty_level": "strong|moderate|weak|crisis",
    "engagement_quality": "above_average|average|below_average",
    "sentiment": "positive|neutral|negative",
    "growth_trajectory": "stable_positive|volatile|declining"
  }},
  "metrics": {{
    "communityHealthScore": 0,
    "loyaltyIndex": 0,
    "engagementQualityScore": 0,
    "sentimentScore": 0,
    "superfanPercentage": 0,
    "responseRateRecommendation": 0,
    "avgEngagementDepth": "surface|light|medium|deep|advocacy",
    "activeEngagersRatio": 0,
    "passiveFollowersRatio": 0,
    "ghostFollowersRatio": 0,
    "commentQualityScore": 0,
    "shareabilityScore": 0,
    "advocacyScore": 0,
    "retentionPrediction": 0,
    "overallScore": 0
  }},
  "findings": [
    "TÜRKÇE Bulgu 1: örn: Topluluk sağlık skoru %65 ile ortalamanın üzerinde ancak süperfan oranı sadece %2.3 - bu uzun vadeli sadakat için risk oluşturuyor. Takipçilerin %78'i pasif, hiç yorum yapmıyor",
    "TÜRKÇE Bulgu 2: örn: Yorum sentiment analizi %72 pozitif gösteriyor ancak yorum derinliği düşük - çoğu emoji veya tek kelimelik tepkiler. Gerçek sohbet başlatan post oranı sadece %8"
  ],
  "recommendations": [
    "TÜRKÇE Öneri 1: Haftalık 'Soru-Cevap' story serisi başlatarak takipçi etkileşimini derinleştirin. Her Cuma 'Takipçi Spotlight' yapın - en aktif takipçiyi öne çıkarın. Beklenen etki: Süperfan oranında %50 artış",
    "TÜRKÇE Öneri 2: Her posta 'tartışma sorusu' ekleyin ve ilk 5 yoruma kişiselleştirilmiş yanıt verin. Yorum yanıt oranını %80'e çıkarın. Beklenen etki: Ortalama yorum sayısında 3x artış"
  ],
  "communityInsights": {{
    "estimatedSuperfans": 0,
    "activeEngagers": 0,
    "passiveFollowers": 0,
    "ghostFollowers": 0,
    "engagementPeakTimes": ["09:00", "19:00"],
    "topEngagementTriggers": ["tetikleyici1", "tetikleyici2"],
    "communityPersonality": {{
      "dominant_trait": "supportive|critical|curious|silent",
      "communication_style": "casual_friendly|formal|mixed",
      "value_seeking": "education|entertainment|community|offers"
    }}
  }},
  "engagementStrategies": [
    {{
      "strategy": "strateji_adı",
      "description": "detaylı_açıklama",
      "expectedImpact": "+%20 engagement gibi",
      "effort": "low|medium|high",
      "timeline": "immediate|weekly|monthly|quarterly"
    }}
  ],
  "communityRituals": [
    {{
      "frequency": "daily|weekly|monthly",
      "ritual": "ritüel_adı",
      "description": "açıklama",
      "purpose": "amaç"
    }}
  ],
  "loyaltyBuilders": [
    {{
      "action": "aksiyon_adı",
      "description": "açıklama",
      "impact": "beklenen_etki",
      "effort": "low|medium|high"
    }}
  ],
  "sentiment_breakdown": {{
    "very_positive": "25%",
    "positive": "45%",
    "neutral": "20%",
    "negative": "8%",
    "very_negative": "2%",
    "trend": "improving|stable_positive|declining|volatile",
    "key_positive_themes": ["tema1", "tema2"],
    "key_concerns": ["endişe1", "endişe2"]
  }},
  "action_plan": {{
    "immediate": ["hemen_yapılacak_1", "hemen_yapılacak_2"],
    "short_term": ["kısa_vade_1", "kısa_vade_2"],
    "long_term": ["uzun_vade_1", "uzun_vade_2"]
  }},
  "edge_case_detection": {{
    "detected_case": "none|new_account|post_viral|niche_change|crisis|engagement_pod|b2b|celebrity|seasonal",
    "special_considerations": ["özel_durum_1"],
    "adjusted_approach": "uyarlanan_yaklaşım_açıklaması"
  }}
}}
```

=== KRİTİK KURALLAR ===
- Metrikleri formüllere göre HESAPLA, rastgele değer verme
- Takipçi sayısına göre benchmark'ları kullan
- Edge case varsa yaklaşımı ona göre ayarla
- SADECE JSON çıktısı ver, başka hiçbir şey yazma
"""

	# analyze metodu BaseAgent'tan miras alınıyor - override edilmemeli
	# BaseAgent.analyze() metodu doğru şekilde:
	# 1. get_system_prompt() ve get_analysis_prompt() çağırır
	# 2. LLM'e istek gönderir
	# 3. Response'u parse eder ve validate eder


__all__ = ["CommunityLoyaltyAgent"]
