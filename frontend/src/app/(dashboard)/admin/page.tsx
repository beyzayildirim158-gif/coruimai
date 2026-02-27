"use client";

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { 
  UsersIcon, 
  PlusIcon, 
  SearchIcon, 
  EditIcon, 
  TrashIcon, 
  KeyIcon,
  ShieldCheckIcon,
  AlertTriangleIcon,
  BarChart3Icon,
  LoaderIcon,
  CheckCircleIcon,
  XCircleIcon,
} from '@/components/icons';
import toast from 'react-hot-toast';
import { useTranslation } from '@/i18n/TranslationProvider';

// Types
interface AdminUser {
  id: string;
  email: string;
  name: string;
  phone: string | null;
  avatarUrl: string | null;
  isAdmin: boolean;
  emailVerified: boolean;
  subscriptionTier: string;
  subscriptionStatus: string;
  createdAt: string;
  lastLoginAt: string | null;
  _count: {
    analyses: number;
    reports: number;
  };
}

interface AdminStats {
  totalUsers: number;
  activeUsers: number;
  totalAnalyses: number;
  totalReports: number;
  usersByTier: Record<string, number>;
  recentUsers: Array<{
    id: string;
    email: string;
    name: string;
    subscriptionTier: string;
    createdAt: string;
  }>;
  recentAnalyses: Array<{
    id: string;
    status: string;
    createdAt: string;
    account: { username: string };
    user: { email: string };
  }>;
}

// Modals
function CreateUserModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const queryClient = useQueryClient();
  const { locale } = useTranslation();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    phone: '',
    subscriptionTier: 'STARTER',
    isAdmin: false,
  });

  const createMutation = useMutation({
    mutationFn: async (data: typeof formData) => {
      const response = await api.post('/admin/users', data);
      return response.data;
    },
    onSuccess: () => {
      toast.success(locale === 'tr' ? 'Kullanıcı oluşturuldu' : 'User created');
      queryClient.invalidateQueries({ queryKey: ['admin', 'users'] });
      queryClient.invalidateQueries({ queryKey: ['admin', 'stats'] });
      onClose();
      setFormData({
        email: '',
        password: '',
        name: '',
        phone: '',
        subscriptionTier: 'STARTER',
        isAdmin: false,
      });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Error creating user');
    },
  });

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold text-slate-900 mb-4">
          {locale === 'tr' ? 'Yeni Kullanıcı Oluştur' : 'Create New User'}
        </h2>
        
        <form onSubmit={(e) => { e.preventDefault(); createMutation.mutate(formData); }} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'E-posta' : 'Email'}
            </label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'Şifre' : 'Password'}
            </label>
            <input
              type="password"
              required
              minLength={8}
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'Ad Soyad' : 'Full Name'}
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'Telefon' : 'Phone'}
            </label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder="+90 5XX XXX XX XX"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'Abonelik Planı' : 'Subscription Tier'}
            </label>
            <select
              value={formData.subscriptionTier}
              onChange={(e) => setFormData({ ...formData, subscriptionTier: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="FREE">FREE</option>
              <option value="STARTER">STARTER</option>
              <option value="PROFESSIONAL">PROFESSIONAL</option>
              <option value="PREMIUM">PREMIUM</option>
              <option value="ENTERPRISE">ENTERPRISE</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="isAdmin"
              checked={formData.isAdmin}
              onChange={(e) => setFormData({ ...formData, isAdmin: e.target.checked })}
              className="rounded border-slate-300 text-primary focus:ring-primary"
            />
            <label htmlFor="isAdmin" className="text-sm text-slate-700">
              {locale === 'tr' ? 'Admin yetkisi ver' : 'Grant admin access'}
            </label>
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-slate-200 rounded-lg text-slate-700 hover:bg-slate-50"
            >
              {locale === 'tr' ? 'İptal' : 'Cancel'}
            </button>
            <button
              type="submit"
              disabled={createMutation.isPending}
              className="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50"
            >
              {createMutation.isPending ? <LoaderIcon className="animate-spin mx-auto" size={20} /> : (locale === 'tr' ? 'Oluştur' : 'Create')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function EditUserModal({ user, isOpen, onClose }: { user: AdminUser | null; isOpen: boolean; onClose: () => void }) {
  const queryClient = useQueryClient();
  const { locale } = useTranslation();
  const [formData, setFormData] = useState({
    email: user?.email || '',
    name: user?.name || '',
    phone: user?.phone || '',
    subscriptionTier: user?.subscriptionTier || 'STARTER',
    subscriptionStatus: user?.subscriptionStatus || 'ACTIVE',
    isAdmin: user?.isAdmin || false,
    emailVerified: user?.emailVerified || false,
  });

  const updateMutation = useMutation({
    mutationFn: async (data: typeof formData) => {
      const response = await api.patch(`/admin/users/${user?.id}`, data);
      return response.data;
    },
    onSuccess: () => {
      toast.success(locale === 'tr' ? 'Kullanıcı güncellendi' : 'User updated');
      queryClient.invalidateQueries({ queryKey: ['admin', 'users'] });
      onClose();
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Error updating user');
    },
  });

  // Update form when user changes
  useState(() => {
    if (user) {
      setFormData({
        email: user.email,
        name: user.name,
        phone: user.phone || '',
        subscriptionTier: user.subscriptionTier,
        subscriptionStatus: user.subscriptionStatus,
        isAdmin: user.isAdmin,
        emailVerified: user.emailVerified,
      });
    }
  });

  if (!isOpen || !user) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold text-slate-900 mb-4">
          {locale === 'tr' ? 'Kullanıcıyı Düzenle' : 'Edit User'}
        </h2>
        
        <form onSubmit={(e) => { e.preventDefault(); updateMutation.mutate(formData); }} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'E-posta' : 'Email'}
            </label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'Ad Soyad' : 'Full Name'}
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'Telefon' : 'Phone'}
            </label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder="+90 5XX XXX XX XX"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'Abonelik Planı' : 'Subscription Tier'}
            </label>
            <select
              value={formData.subscriptionTier}
              onChange={(e) => setFormData({ ...formData, subscriptionTier: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="FREE">FREE</option>
              <option value="STARTER">STARTER</option>
              <option value="PROFESSIONAL">PROFESSIONAL</option>
              <option value="PREMIUM">PREMIUM</option>
              <option value="ENTERPRISE">ENTERPRISE</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'Abonelik Durumu' : 'Subscription Status'}
            </label>
            <select
              value={formData.subscriptionStatus}
              onChange={(e) => setFormData({ ...formData, subscriptionStatus: e.target.value })}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="ACTIVE">ACTIVE</option>
              <option value="TRIALING">TRIALING</option>
              <option value="PAUSED">PAUSED</option>
              <option value="PAST_DUE">PAST_DUE</option>
              <option value="CANCELLED">CANCELLED</option>
            </select>
          </div>

          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={formData.isAdmin}
                onChange={(e) => setFormData({ ...formData, isAdmin: e.target.checked })}
                className="rounded border-slate-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-slate-700">{locale === 'tr' ? 'Admin' : 'Admin'}</span>
            </label>
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={formData.emailVerified}
                onChange={(e) => setFormData({ ...formData, emailVerified: e.target.checked })}
                className="rounded border-slate-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-slate-700">{locale === 'tr' ? 'E-posta Doğrulandı' : 'Email Verified'}</span>
            </label>
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-slate-200 rounded-lg text-slate-700 hover:bg-slate-50"
            >
              {locale === 'tr' ? 'İptal' : 'Cancel'}
            </button>
            <button
              type="submit"
              disabled={updateMutation.isPending}
              className="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50"
            >
              {updateMutation.isPending ? <LoaderIcon className="animate-spin mx-auto" size={20} /> : (locale === 'tr' ? 'Kaydet' : 'Save')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function ChangePasswordModal({ user, isOpen, onClose }: { user: AdminUser | null; isOpen: boolean; onClose: () => void }) {
  const queryClient = useQueryClient();
  const { locale } = useTranslation();
  const [newPassword, setNewPassword] = useState('');

  const changeMutation = useMutation({
    mutationFn: async () => {
      const response = await api.patch(`/admin/users/${user?.id}/password`, { newPassword });
      return response.data;
    },
    onSuccess: () => {
      toast.success(locale === 'tr' ? 'Şifre değiştirildi' : 'Password changed');
      onClose();
      setNewPassword('');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Error changing password');
    },
  });

  if (!isOpen || !user) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl p-6 w-full max-w-md">
        <h2 className="text-xl font-bold text-slate-900 mb-4">
          {locale === 'tr' ? 'Şifre Değiştir' : 'Change Password'}
        </h2>
        <p className="text-sm text-slate-500 mb-4">
          {user.email}
        </p>
        
        <form onSubmit={(e) => { e.preventDefault(); changeMutation.mutate(); }} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {locale === 'tr' ? 'Yeni Şifre' : 'New Password'}
            </label>
            <input
              type="password"
              required
              minLength={8}
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder="••••••••"
            />
            <p className="text-xs text-slate-500 mt-1">
              {locale === 'tr' ? 'Minimum 8 karakter' : 'Minimum 8 characters'}
            </p>
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-slate-200 rounded-lg text-slate-700 hover:bg-slate-50"
            >
              {locale === 'tr' ? 'İptal' : 'Cancel'}
            </button>
            <button
              type="submit"
              disabled={changeMutation.isPending}
              className="flex-1 px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 disabled:opacity-50"
            >
              {changeMutation.isPending ? <LoaderIcon className="animate-spin mx-auto" size={20} /> : (locale === 'tr' ? 'Değiştir' : 'Change')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function DeleteUserModal({ user, isOpen, onClose }: { user: AdminUser | null; isOpen: boolean; onClose: () => void }) {
  const queryClient = useQueryClient();
  const { locale } = useTranslation();

  const deleteMutation = useMutation({
    mutationFn: async () => {
      const response = await api.delete(`/admin/users/${user?.id}`);
      return response.data;
    },
    onSuccess: () => {
      toast.success(locale === 'tr' ? 'Kullanıcı silindi' : 'User deleted');
      queryClient.invalidateQueries({ queryKey: ['admin', 'users'] });
      queryClient.invalidateQueries({ queryKey: ['admin', 'stats'] });
      onClose();
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Error deleting user');
    },
  });

  if (!isOpen || !user) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl p-6 w-full max-w-md">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-red-100 rounded-full">
            <AlertTriangleIcon size={24} className="text-red-600" />
          </div>
          <h2 className="text-xl font-bold text-slate-900">
            {locale === 'tr' ? 'Kullanıcıyı Sil' : 'Delete User'}
          </h2>
        </div>
        
        <p className="text-slate-600 mb-2">
          {locale === 'tr' 
            ? 'Bu kullanıcıyı silmek istediğinizden emin misiniz?' 
            : 'Are you sure you want to delete this user?'}
        </p>
        <p className="text-sm text-slate-500 mb-4">
          <strong>{user.email}</strong> - {user.name}
        </p>
        <p className="text-sm text-red-600 mb-4">
          {locale === 'tr' 
            ? 'Bu işlem geri alınamaz. Kullanıcının tüm verileri silinecektir.' 
            : 'This action cannot be undone. All user data will be deleted.'}
        </p>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 border border-slate-200 rounded-lg text-slate-700 hover:bg-slate-50"
          >
            {locale === 'tr' ? 'İptal' : 'Cancel'}
          </button>
          <button
            onClick={() => deleteMutation.mutate()}
            disabled={deleteMutation.isPending}
            className="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50"
          >
            {deleteMutation.isPending ? <LoaderIcon className="animate-spin mx-auto" size={20} /> : (locale === 'tr' ? 'Sil' : 'Delete')}
          </button>
        </div>
      </div>
    </div>
  );
}

// Main Admin Page
export default function AdminPage() {
  const { user } = useAuthStore();
  const router = useRouter();
  const { locale } = useTranslation();
  
  const [searchQuery, setSearchQuery] = useState('');
  const [filterTier, setFilterTier] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [page, setPage] = useState(1);
  
  // Modals
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingUser, setEditingUser] = useState<AdminUser | null>(null);
  const [passwordUser, setPasswordUser] = useState<AdminUser | null>(null);
  const [deletingUser, setDeletingUser] = useState<AdminUser | null>(null);

  // Check admin access
  const statsQuery = useQuery({
    queryKey: ['admin', 'stats'],
    queryFn: async () => {
      const response = await api.get('/admin/stats');
      return response.data.data as AdminStats;
    },
  });

  const usersQuery = useQuery({
    queryKey: ['admin', 'users', { page, search: searchQuery, tier: filterTier, status: filterStatus }],
    queryFn: async () => {
      const params = new URLSearchParams();
      params.set('page', page.toString());
      params.set('limit', '10');
      if (searchQuery) params.set('search', searchQuery);
      if (filterTier) params.set('tier', filterTier);
      if (filterStatus) params.set('status', filterStatus);
      
      const response = await api.get(`/admin/users?${params.toString()}`);
      return response.data.data;
    },
  });

  // Redirect non-admins
  if (statsQuery.isError || usersQuery.isError) {
    return (
      <div className="rounded-2xl sm:rounded-3xl border border-red-200 bg-red-50 p-6 sm:p-8 text-center">
        <AlertTriangleIcon size={48} className="mx-auto text-red-500 mb-4" />
        <h2 className="text-xl font-bold text-red-700 mb-2">
          {locale === 'tr' ? 'Erişim Reddedildi' : 'Access Denied'}
        </h2>
        <p className="text-red-600">
          {locale === 'tr' 
            ? 'Bu sayfaya erişim yetkiniz yok.' 
            : 'You do not have permission to access this page.'}
        </p>
      </div>
    );
  }

  const stats = statsQuery.data;
  const users = usersQuery.data?.users as AdminUser[] || [];
  const pagination = usersQuery.data?.pagination;

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Header */}
      <div className="rounded-2xl sm:rounded-3xl bg-gradient-to-r from-slate-800 to-slate-900 p-4 sm:p-6 text-white">
        <div className="flex items-center gap-3">
          <div className="p-2 sm:p-3 bg-white/10 rounded-xl sm:rounded-2xl">
            <ShieldCheckIcon size={24} className="sm:hidden" />
            <ShieldCheckIcon size={32} className="hidden sm:block" />
          </div>
          <div>
            <p className="text-xs sm:text-sm uppercase tracking-wider text-white/60">
              {locale === 'tr' ? 'Yönetim Paneli' : 'Admin Panel'}
            </p>
            <h1 className="text-xl sm:text-2xl font-bold">
              {locale === 'tr' ? 'Kullanıcı Yönetimi' : 'User Management'}
            </h1>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
          <div className="rounded-xl sm:rounded-2xl border border-slate-200 bg-white p-4 sm:p-5">
            <div className="flex items-center gap-2 text-slate-500 mb-2">
              <UsersIcon size={16} />
              <span className="text-xs uppercase tracking-wider">
                {locale === 'tr' ? 'Toplam Kullanıcı' : 'Total Users'}
              </span>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900">{stats.totalUsers}</p>
          </div>
          <div className="rounded-xl sm:rounded-2xl border border-slate-200 bg-white p-4 sm:p-5">
            <div className="flex items-center gap-2 text-slate-500 mb-2">
              <CheckCircleIcon size={16} />
              <span className="text-xs uppercase tracking-wider">
                {locale === 'tr' ? 'Aktif Kullanıcı' : 'Active Users'}
              </span>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-green-600">{stats.activeUsers}</p>
          </div>
          <div className="rounded-xl sm:rounded-2xl border border-slate-200 bg-white p-4 sm:p-5">
            <div className="flex items-center gap-2 text-slate-500 mb-2">
              <BarChart3Icon size={16} />
              <span className="text-xs uppercase tracking-wider">
                {locale === 'tr' ? 'Toplam Analiz' : 'Total Analyses'}
              </span>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900">{stats.totalAnalyses}</p>
          </div>
          <div className="rounded-xl sm:rounded-2xl border border-slate-200 bg-white p-4 sm:p-5">
            <div className="flex items-center gap-2 text-slate-500 mb-2">
              <BarChart3Icon size={16} />
              <span className="text-xs uppercase tracking-wider">
                {locale === 'tr' ? 'Toplam Rapor' : 'Total Reports'}
              </span>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900">{stats.totalReports}</p>
          </div>
        </div>
      )}

      {/* User Management */}
      <div className="rounded-2xl sm:rounded-3xl border border-slate-200 bg-white shadow-sm">
        {/* Toolbar */}
        <div className="p-4 border-b border-slate-200">
          <div className="flex flex-col sm:flex-row gap-3">
            {/* Search */}
            <div className="relative flex-1">
              <SearchIcon size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => { setSearchQuery(e.target.value); setPage(1); }}
                placeholder={locale === 'tr' ? 'E-posta, isim veya telefon ara...' : 'Search email, name or phone...'}
                className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
              />
            </div>
            
            {/* Filters */}
            <div className="flex gap-2">
              <select
                value={filterTier}
                onChange={(e) => { setFilterTier(e.target.value); setPage(1); }}
                className="px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
              >
                <option value="">{locale === 'tr' ? 'Tüm Planlar' : 'All Tiers'}</option>
                <option value="FREE">FREE</option>
                <option value="STARTER">STARTER</option>
                <option value="PROFESSIONAL">PROFESSIONAL</option>
                <option value="PREMIUM">PREMIUM</option>
                <option value="ENTERPRISE">ENTERPRISE</option>
              </select>
              
              <select
                value={filterStatus}
                onChange={(e) => { setFilterStatus(e.target.value); setPage(1); }}
                className="px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
              >
                <option value="">{locale === 'tr' ? 'Tüm Durumlar' : 'All Status'}</option>
                <option value="ACTIVE">ACTIVE</option>
                <option value="TRIALING">TRIALING</option>
                <option value="PAUSED">PAUSED</option>
                <option value="PAST_DUE">PAST_DUE</option>
                <option value="CANCELLED">CANCELLED</option>
              </select>
            </div>
            
            {/* Create Button */}
            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center justify-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 text-sm font-medium"
            >
              <PlusIcon size={18} />
              <span className="hidden sm:inline">{locale === 'tr' ? 'Yeni Kullanıcı' : 'New User'}</span>
            </button>
          </div>
        </div>

        {/* Users Table */}
        <div className="overflow-x-auto">
          {usersQuery.isLoading ? (
            <div className="flex items-center justify-center py-12">
              <LoaderIcon size={24} className="animate-spin text-slate-400" />
            </div>
          ) : users.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              {locale === 'tr' ? 'Kullanıcı bulunamadı' : 'No users found'}
            </div>
          ) : (
            <table className="w-full">
              <thead className="bg-slate-50 text-left text-xs uppercase tracking-wider text-slate-500">
                <tr>
                  <th className="px-4 py-3">{locale === 'tr' ? 'Kullanıcı' : 'User'}</th>
                  <th className="px-4 py-3 hidden md:table-cell">{locale === 'tr' ? 'Telefon' : 'Phone'}</th>
                  <th className="px-4 py-3">{locale === 'tr' ? 'Plan' : 'Tier'}</th>
                  <th className="px-4 py-3 hidden sm:table-cell">{locale === 'tr' ? 'Durum' : 'Status'}</th>
                  <th className="px-4 py-3 hidden lg:table-cell">{locale === 'tr' ? 'Analizler' : 'Analyses'}</th>
                  <th className="px-4 py-3 text-right">{locale === 'tr' ? 'İşlemler' : 'Actions'}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-slate-200 flex items-center justify-center text-slate-600 font-medium text-sm">
                          {u.name.charAt(0).toUpperCase()}
                        </div>
                        <div className="min-w-0">
                          <div className="flex items-center gap-2">
                            <p className="text-sm font-medium text-slate-900 truncate">{u.name}</p>
                            {u.isAdmin && (
                              <span className="px-1.5 py-0.5 text-xs bg-purple-100 text-purple-700 rounded">Admin</span>
                            )}
                          </div>
                          <p className="text-xs text-slate-500 truncate">{u.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3 hidden md:table-cell">
                      <span className="text-sm text-slate-600">{u.phone || '-'}</span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                        u.subscriptionTier === 'ENTERPRISE' ? 'bg-purple-100 text-purple-700' :
                        u.subscriptionTier === 'PREMIUM' ? 'bg-amber-100 text-amber-700' :
                        u.subscriptionTier === 'PROFESSIONAL' ? 'bg-blue-100 text-blue-700' :
                        u.subscriptionTier === 'STARTER' ? 'bg-green-100 text-green-700' :
                        'bg-slate-100 text-slate-700'
                      }`}>
                        {u.subscriptionTier}
                      </span>
                    </td>
                    <td className="px-4 py-3 hidden sm:table-cell">
                      <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${
                        u.subscriptionStatus === 'ACTIVE' ? 'bg-green-100 text-green-700' :
                        u.subscriptionStatus === 'TRIALING' ? 'bg-blue-100 text-blue-700' :
                        u.subscriptionStatus === 'PAUSED' ? 'bg-amber-100 text-amber-700' :
                        'bg-red-100 text-red-700'
                      }`}>
                        {u.subscriptionStatus === 'ACTIVE' && <CheckCircleIcon size={12} />}
                        {u.subscriptionStatus === 'CANCELLED' && <XCircleIcon size={12} />}
                        {u.subscriptionStatus}
                      </span>
                    </td>
                    <td className="px-4 py-3 hidden lg:table-cell">
                      <span className="text-sm text-slate-600">{u._count.analyses}</span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-end gap-1">
                        <button
                          onClick={() => setEditingUser(u)}
                          className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition"
                          title={locale === 'tr' ? 'Düzenle' : 'Edit'}
                        >
                          <EditIcon size={16} />
                        </button>
                        <button
                          onClick={() => setPasswordUser(u)}
                          className="p-2 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition"
                          title={locale === 'tr' ? 'Şifre Değiştir' : 'Change Password'}
                        >
                          <KeyIcon size={16} />
                        </button>
                        <button
                          onClick={() => setDeletingUser(u)}
                          className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                          title={locale === 'tr' ? 'Sil' : 'Delete'}
                        >
                          <TrashIcon size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Pagination */}
        {pagination && pagination.totalPages > 1 && (
          <div className="p-4 border-t border-slate-200 flex items-center justify-between">
            <p className="text-sm text-slate-500">
              {locale === 'tr' 
                ? `${pagination.total} kullanıcıdan ${(pagination.page - 1) * pagination.limit + 1}-${Math.min(pagination.page * pagination.limit, pagination.total)} arası gösteriliyor`
                : `Showing ${(pagination.page - 1) * pagination.limit + 1}-${Math.min(pagination.page * pagination.limit, pagination.total)} of ${pagination.total} users`}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setPage(page - 1)}
                disabled={page === 1}
                className="px-3 py-1 border border-slate-200 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
              >
                {locale === 'tr' ? 'Önceki' : 'Previous'}
              </button>
              <button
                onClick={() => setPage(page + 1)}
                disabled={page === pagination.totalPages}
                className="px-3 py-1 border border-slate-200 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
              >
                {locale === 'tr' ? 'Sonraki' : 'Next'}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Modals */}
      <CreateUserModal isOpen={showCreateModal} onClose={() => setShowCreateModal(false)} />
      <EditUserModal user={editingUser} isOpen={!!editingUser} onClose={() => setEditingUser(null)} />
      <ChangePasswordModal user={passwordUser} isOpen={!!passwordUser} onClose={() => setPasswordUser(null)} />
      <DeleteUserModal user={deletingUser} isOpen={!!deletingUser} onClose={() => setDeletingUser(null)} />
    </div>
  );
}
