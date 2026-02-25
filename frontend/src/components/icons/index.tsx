'use client';

import { Icon, type IconProps as IconifyIconProps } from '@iconify/react';
import { forwardRef } from 'react';

// Common props type for all icons
interface IconProps extends Omit<IconifyIconProps, 'icon' | 'width' | 'height'> {
  size?: number | string;
}

// Solar icons - Bold style for filled, Linear for outline
// Phosphor icons - Bold, Regular, Duotone styles

// ===== NAVIGATION & UI ICONS =====

export const HomeIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:home-2-bold" className={className} width={size} height={size} {...props} />
));
HomeIcon.displayName = 'HomeIcon';

export const ActivityIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:pulse-2-bold" className={className} width={size} height={size} {...props} />
));
ActivityIcon.displayName = 'ActivityIcon';

export const FileTextIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:document-text-bold" className={className} width={size} height={size} {...props} />
));
FileTextIcon.displayName = 'FileTextIcon';

export const BarChart3Icon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:chart-bold" className={className} width={size} height={size} {...props} />
));
BarChart3Icon.displayName = 'BarChart3Icon';

export const CreditCardIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:card-bold" className={className} width={size} height={size} {...props} />
));
CreditCardIcon.displayName = 'CreditCardIcon';

export const SettingsIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:settings-bold" className={className} width={size} height={size} {...props} />
));
SettingsIcon.displayName = 'SettingsIcon';

export const MenuIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:hamburger-menu-bold" className={className} width={size} height={size} {...props} />
));
MenuIcon.displayName = 'MenuIcon';

export const SearchIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:magnifer-bold" className={className} width={size} height={size} {...props} />
));
SearchIcon.displayName = 'SearchIcon';

export const BellIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:bell-bold" className={className} width={size} height={size} {...props} />
));
BellIcon.displayName = 'BellIcon';

export const CloseIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:close-circle-bold" className={className} width={size} height={size} {...props} />
));
CloseIcon.displayName = 'CloseIcon';

export const LogOutIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:logout-2-bold" className={className} width={size} height={size} {...props} />
));
LogOutIcon.displayName = 'LogOutIcon';

export const ChevronDownIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:alt-arrow-down-bold" className={className} width={size} height={size} {...props} />
));
ChevronDownIcon.displayName = 'ChevronDownIcon';

export const ChevronUpIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:alt-arrow-up-bold" className={className} width={size} height={size} {...props} />
));
ChevronUpIcon.displayName = 'ChevronUpIcon';

export const ChevronLeftIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:alt-arrow-left-bold" className={className} width={size} height={size} {...props} />
));
ChevronLeftIcon.displayName = 'ChevronLeftIcon';

export const ChevronRightIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:alt-arrow-right-bold" className={className} width={size} height={size} {...props} />
));
ChevronRightIcon.displayName = 'ChevronRightIcon';

export const ArrowRightIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:arrow-right-bold" className={className} width={size} height={size} {...props} />
));
ArrowRightIcon.displayName = 'ArrowRightIcon';

export const ArrowUpRightIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:arrow-right-up-bold" className={className} width={size} height={size} {...props} />
));
ArrowUpRightIcon.displayName = 'ArrowUpRightIcon';

export const GlobeIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:global-bold" className={className} width={size} height={size} {...props} />
));
GlobeIcon.displayName = 'GlobeIcon';

export const ExternalLinkIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:square-arrow-right-up-bold" className={className} width={size} height={size} {...props} />
));
ExternalLinkIcon.displayName = 'ExternalLinkIcon';

export const DownloadIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:download-bold" className={className} width={size} height={size} {...props} />
));
DownloadIcon.displayName = 'DownloadIcon';

export const CopyIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:copy-bold" className={className} width={size} height={size} {...props} />
));
CopyIcon.displayName = 'CopyIcon';

export const CheckIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:check-circle-bold" className={className} width={size} height={size} {...props} />
));
CheckIcon.displayName = 'CheckIcon';

export const RefreshIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:refresh-bold" className={className} width={size} height={size} {...props} />
));
RefreshIcon.displayName = 'RefreshIcon';

// ===== AGENT & ANALYSIS ICONS =====

// Domain Master - Sector & Niche Analysis
export const TargetIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:target-bold" className={className} width={size} height={size} {...props} />
));
TargetIcon.displayName = 'TargetIcon';

// Growth & Virality - Trending Analysis
export const TrendingUpIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:graph-up-bold" className={className} width={size} height={size} {...props} />
));
TrendingUpIcon.displayName = 'TrendingUpIcon';

// Sales & Conversion - Monetization
export const DollarSignIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:dollar-bold" className={className} width={size} height={size} {...props} />
));
DollarSignIcon.displayName = 'DollarSignIcon';

// Visual Brand - Design & Aesthetics
export const PaletteIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:pallete-2-bold" className={className} width={size} height={size} {...props} />
));
PaletteIcon.displayName = 'PaletteIcon';

// Community Loyalty - Heart & Engagement
export const HeartIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:heart-bold" className={className} width={size} height={size} {...props} />
));
HeartIcon.displayName = 'HeartIcon';

// Attention Architect - Eye & Focus
export const EyeIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:eye-bold" className={className} width={size} height={size} {...props} />
));
EyeIcon.displayName = 'EyeIcon';

// System Governor - Security & Validation
export const ShieldIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:shield-check-bold" className={className} width={size} height={size} {...props} />
));
ShieldIcon.displayName = 'ShieldIcon';

export const ShieldCheckIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:verified-check-bold" className={className} width={size} height={size} {...props} />
));
ShieldCheckIcon.displayName = 'ShieldCheckIcon';

// Users & Community
export const UsersIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:users-group-rounded-bold" className={className} width={size} height={size} {...props} />
));
UsersIcon.displayName = 'UsersIcon';

export const UserIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:user-bold" className={className} width={size} height={size} {...props} />
));
UserIcon.displayName = 'UserIcon';

// ===== AI & SPECIAL ICONS (NO STANDARD AI ICONS!) =====

// Magic Wand for AI/Analysis - NOT standard AI brain icon
export const MagicWandIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:magic-stick-3-bold" className={className} width={size} height={size} {...props} />
));
MagicWandIcon.displayName = 'MagicWandIcon';

// Spark for AI features
export const SparkIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:stars-bold" className={className} width={size} height={size} {...props} />
));
SparkIcon.displayName = 'SparkIcon';

// Atom for advanced analysis
export const AtomIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:atom-bold" className={className} width={size} height={size} {...props} />
));
AtomIcon.displayName = 'AtomIcon';

// Lightning for fast/power features (Zap replacement)
export const LightningIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:bolt-bold" className={className} width={size} height={size} {...props} />
));
LightningIcon.displayName = 'LightningIcon';

// Rocket for growth
export const RocketIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:rocket-2-bold" className={className} width={size} height={size} {...props} />
));
RocketIcon.displayName = 'RocketIcon';

// Diamond for premium/value
export const DiamondIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:diamond-bold" className={className} width={size} height={size} {...props} />
));
DiamondIcon.displayName = 'DiamondIcon';

// Crown for premium tiers
export const CrownIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:crown-bold" className={className} width={size} height={size} {...props} />
));
CrownIcon.displayName = 'CrownIcon';

// Fire for hot/trending content
export const FireIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:fire-bold" className={className} width={size} height={size} {...props} />
));
FireIcon.displayName = 'FireIcon';

// ===== STATUS & FEEDBACK ICONS =====

export const InfoIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:info-circle-bold" className={className} width={size} height={size} {...props} />
));
InfoIcon.displayName = 'InfoIcon';

export const WarningIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:danger-triangle-bold" className={className} width={size} height={size} {...props} />
));
WarningIcon.displayName = 'WarningIcon';

export const AlertTriangleIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:danger-triangle-bold" className={className} width={size} height={size} {...props} />
));
AlertTriangleIcon.displayName = 'AlertTriangleIcon';

export const CheckCircleIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:check-circle-bold" className={className} width={size} height={size} {...props} />
));
CheckCircleIcon.displayName = 'CheckCircleIcon';

// ===== CONTENT & MEDIA ICONS =====

export const PhotoIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:gallery-bold" className={className} width={size} height={size} {...props} />
));
PhotoIcon.displayName = 'PhotoIcon';

export const VideoIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:video-frame-play-bold" className={className} width={size} height={size} {...props} />
));
VideoIcon.displayName = 'VideoIcon';

export const ReelsIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:clapperboard-play-bold" className={className} width={size} height={size} {...props} />
));
ReelsIcon.displayName = 'ReelsIcon';

export const HashtagIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:hashtag-bold" className={className} width={size} height={size} {...props} />
));
HashtagIcon.displayName = 'HashtagIcon';

export const CalendarIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:calendar-bold" className={className} width={size} height={size} {...props} />
));
CalendarIcon.displayName = 'CalendarIcon';

export const ClockIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:clock-circle-bold" className={className} width={size} height={size} {...props} />
));
ClockIcon.displayName = 'ClockIcon';

export const TimerIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:stopwatch-bold" className={className} width={size} height={size} {...props} />
));
TimerIcon.displayName = 'TimerIcon';

export const CalendarDaysIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:calendar-bold" className={className} width={size} height={size} {...props} />
));
CalendarDaysIcon.displayName = 'CalendarDaysIcon';

export const CalendarRangeIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:calendar-date-bold" className={className} width={size} height={size} {...props} />
));
CalendarRangeIcon.displayName = 'CalendarRangeIcon';

export const CircleIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:record-circle-bold" className={className} width={size} height={size} {...props} />
));
CircleIcon.displayName = 'CircleIcon';

export const FilmIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:clapperboard-play-bold" className={className} width={size} height={size} {...props} />
));
FilmIcon.displayName = 'FilmIcon';

export const LayersIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:layers-bold" className={className} width={size} height={size} {...props} />
));
LayersIcon.displayName = 'LayersIcon';

export const ImageIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:gallery-bold" className={className} width={size} height={size} {...props} />
));
ImageIcon.displayName = 'ImageIcon';

export const AlertCircleIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:danger-circle-bold" className={className} width={size} height={size} {...props} />
));
AlertCircleIcon.displayName = 'AlertCircleIcon';

export const BookOpenIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:book-2-bold" className={className} width={size} height={size} {...props} />
));
BookOpenIcon.displayName = 'BookOpenIcon';

export const SmileIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:emoji-funny-circle-bold" className={className} width={size} height={size} {...props} />
));
SmileIcon.displayName = 'SmileIcon';

export const ShoppingBagIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:bag-bold" className={className} width={size} height={size} {...props} />
));
ShoppingBagIcon.displayName = 'ShoppingBagIcon';

export const WrenchIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:wrench-bold" className={className} width={size} height={size} {...props} />
));
WrenchIcon.displayName = 'WrenchIcon';

export const ShieldAlertIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:shield-warning-bold" className={className} width={size} height={size} {...props} />
));
ShieldAlertIcon.displayName = 'ShieldAlertIcon';

export const BotIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:cpu-bold" className={className} width={size} height={size} {...props} />
));
BotIcon.displayName = 'BotIcon';

export const MinusIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:minus-bold" className={className} width={size} height={size} {...props} />
));
MinusIcon.displayName = 'MinusIcon';

export const XCircleIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:close-circle-bold" className={className} width={size} height={size} {...props} />
));
XCircleIcon.displayName = 'XCircleIcon';

export const BookmarkIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:bookmark-bold" className={className} width={size} height={size} {...props} />
));
BookmarkIcon.displayName = 'BookmarkIcon';

export const ShareIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:share-bold" className={className} width={size} height={size} {...props} />
));
ShareIcon.displayName = 'ShareIcon';

export const CommentIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:chat-round-dots-bold" className={className} width={size} height={size} {...props} />
));
CommentIcon.displayName = 'CommentIcon';

export const MapPinIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:map-point-bold" className={className} width={size} height={size} {...props} />
));
MapPinIcon.displayName = 'MapPinIcon';

export const GiftIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:gift-bold" className={className} width={size} height={size} {...props} />
));
GiftIcon.displayName = 'GiftIcon';

// ===== ANALYTICS & CHART ICONS =====

export const ChartIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:chart-2-bold" className={className} width={size} height={size} {...props} />
));
ChartIcon.displayName = 'ChartIcon';

export const GaugeIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:tuning-4-bold" className={className} width={size} height={size} {...props} />
));
GaugeIcon.displayName = 'GaugeIcon';

export const RadarIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:radar-bold" className={className} width={size} height={size} {...props} />
));
RadarIcon.displayName = 'RadarIcon';

export const LightbulbIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:lightbulb-bolt-bold" className={className} width={size} height={size} {...props} />
));
LightbulbIcon.displayName = 'LightbulbIcon';

// ===== LOADING & SPINNER =====

export const LoaderIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:refresh-bold" className={`animate-spin ${className || ''}`} width={size} height={size} {...props} />
));
LoaderIcon.displayName = 'LoaderIcon';

// ===== SOCIAL MEDIA ICONS =====

export const InstagramIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="ph:instagram-logo-bold" className={className} width={size} height={size} {...props} />
));
InstagramIcon.displayName = 'InstagramIcon';

// ===== ADDITIONAL UI ICONS =====

export const TrophyIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:cup-bold" className={className} width={size} height={size} {...props} />
));
TrophyIcon.displayName = 'TrophyIcon';

export const BriefcaseIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:case-round-bold" className={className} width={size} height={size} {...props} />
));
BriefcaseIcon.displayName = 'BriefcaseIcon';

export const SaveIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:diskette-bold" className={className} width={size} height={size} {...props} />
));
SaveIcon.displayName = 'SaveIcon';

export const TrashIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:trash-bin-trash-bold" className={className} width={size} height={size} {...props} />
));
TrashIcon.displayName = 'TrashIcon';

export const EyeOffIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:eye-closed-bold" className={className} width={size} height={size} {...props} />
));
EyeOffIcon.displayName = 'EyeOffIcon';

export const DownloadCloudIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:cloud-download-bold" className={className} width={size} height={size} {...props} />
));
DownloadCloudIcon.displayName = 'DownloadCloudIcon';

export const FilterIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:filter-bold" className={className} width={size} height={size} {...props} />
));
FilterIcon.displayName = 'FilterIcon';

export const MailIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:letter-bold" className={className} width={size} height={size} {...props} />
));
MailIcon.displayName = 'MailIcon';

export const MailCheckIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:inbox-line-bold" className={className} width={size} height={size} {...props} />
));
MailCheckIcon.displayName = 'MailCheckIcon';

export const LinkIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:link-bold" className={className} width={size} height={size} {...props} />
));
LinkIcon.displayName = 'LinkIcon';

export const Grid3X3Icon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:widget-5-bold" className={className} width={size} height={size} {...props} />
));
Grid3X3Icon.displayName = 'Grid3X3Icon';

export const UserPlusIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:user-plus-bold" className={className} width={size} height={size} {...props} />
));
UserPlusIcon.displayName = 'UserPlusIcon';

export const ReceiptTextIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:bill-list-bold" className={className} width={size} height={size} {...props} />
));
ReceiptTextIcon.displayName = 'ReceiptTextIcon';

export const StarIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:star-bold" className={className} width={size} height={size} {...props} />
));
StarIcon.displayName = 'StarIcon';

export const AlertOctagonIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:danger-bold" className={className} width={size} height={size} {...props} />
));
AlertOctagonIcon.displayName = 'AlertOctagonIcon';

export const TrendingDownIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:graph-down-bold" className={className} width={size} height={size} {...props} />
));
TrendingDownIcon.displayName = 'TrendingDownIcon';

export const KeyRoundIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:key-bold" className={className} width={size} height={size} {...props} />
));
KeyRoundIcon.displayName = 'KeyRoundIcon';

export const CheckCircle2Icon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:check-circle-bold" className={className} width={size} height={size} {...props} />
));
CheckCircle2Icon.displayName = 'CheckCircle2Icon';

// ===== SECURITY & AUTH ICONS =====

export const KeyIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:key-bold" className={className} width={size} height={size} {...props} />
));
KeyIcon.displayName = 'KeyIcon';

export const LockIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:lock-bold" className={className} width={size} height={size} {...props} />
));
LockIcon.displayName = 'LockIcon';

// ===== BRAND/LOGO ICON - Custom for App =====

export const AppLogoIcon = forwardRef<SVGSVGElement, IconProps>(({ className, size = 24, ...props }, ref) => (
  <Icon icon="solar:magic-stick-3-bold" className={className} width={size} height={size} {...props} />
));
AppLogoIcon.displayName = 'AppLogoIcon';

// ===== RE-EXPORTS FOR COMPATIBILITY =====

// Map lucide names to our icons
export {
  HomeIcon as Home,
  ActivityIcon as Activity,
  FileTextIcon as FileText,
  BarChart3Icon as BarChart3,
  CreditCardIcon as CreditCard,
  SettingsIcon as Settings,
  SparkIcon as Sparkles,
  MenuIcon as Menu,
  SearchIcon as Search,
  BellIcon as Bell,
  CloseIcon as X,
  LogOutIcon as LogOut,
  ChevronDownIcon as ChevronDown,
  ChevronUpIcon as ChevronUp,
  ArrowUpRightIcon as ArrowUpRight,
  ArrowRightIcon as ArrowRight,
  TargetIcon as Target,
  TrendingUpIcon as TrendingUp,
  DollarSignIcon as DollarSign,
  PaletteIcon as Palette,
  HeartIcon as Heart,
  EyeIcon as Eye,
  ShieldIcon as Shield,
  ShieldCheckIcon as ShieldCheck,
  UsersIcon as Users,
  UserIcon as User,
  LightningIcon as Zap,
  LoaderIcon as Loader2,
  CheckIcon as Check,
  CheckCircleIcon as CheckCircle,
  AlertTriangleIcon as AlertTriangle,
  InfoIcon as Info,
  GlobeIcon as Globe,
  ExternalLinkIcon as ExternalLink,
  DownloadIcon as Download,
  KeyIcon as Key,
  GaugeIcon as Gauge,
  RadarIcon as Radar,
  LightbulbIcon as Lightbulb,
  CalendarIcon as Calendar,
  ChevronLeftIcon as ChevronLeft,
  ChevronRightIcon as ChevronRight,
  CopyIcon as Copy,
  RefreshIcon as RefreshCw,
  VideoIcon as Video,
  PhotoIcon as Photo,
  HashtagIcon as Hash,
  BookmarkIcon as Bookmark,
  ShareIcon as Share,
  CommentIcon as MessageCircle,
  CrownIcon as Crown,
  FireIcon as Fire,
  RocketIcon as Rocket,
  DiamondIcon as Diamond,
  AtomIcon as Atom,
  TrophyIcon as Trophy,
  BriefcaseIcon as Briefcase,
  SaveIcon as Save,
  TrashIcon as Trash2,
  EyeOffIcon as EyeOff,
  DownloadCloudIcon as DownloadCloud,
  FilterIcon as Filter,
  MailIcon as Mail,
  MailCheckIcon as MailCheck,
  LinkIcon as Link,
  Grid3X3Icon as Grid3X3,
  UserPlusIcon as UserPlus,
  ReceiptTextIcon as ReceiptText,
  StarIcon as Star,
  AlertOctagonIcon as AlertOctagon,
  TrendingDownIcon as TrendingDown,
  KeyRoundIcon as KeyRound,
  CheckCircle2Icon as CheckCircle2,
  InstagramIcon as Instagram,
  ClockIcon as Clock,
  TimerIcon as Timer,
  CalendarDaysIcon as CalendarDays,
  CalendarRangeIcon as CalendarRange,
  CircleIcon as Circle,
  FilmIcon as Film,
  LayersIcon as Layers,
  ImageIcon as Image,
  AlertCircleIcon as AlertCircle,
  BookOpenIcon as BookOpen,
  SmileIcon as Smile,
  ShoppingBagIcon as ShoppingBag,
  WrenchIcon as Wrench,
  ShieldAlertIcon as ShieldAlert,
  BotIcon as Bot,
  MinusIcon as Minus,
  XCircleIcon as XCircle,
};
