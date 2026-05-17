import axios from 'axios';
import type { Novel, DownloadTask } from '../types';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Health check
export const healthCheck = async (): Promise<boolean> => {
  try {
    const response = await api.get('/health');
    return response.status === 200;
  } catch {
    return false;
  }
};

// ============================================
// DOWNLOADS
// ============================================

export const startDownload = async (url: string): Promise<DownloadTask> => {
  const response = await api.post<DownloadTask>('/downloads', { url });
  return response.data;
};

export const getDownloads = async (status?: string): Promise<DownloadTask[]> => {
  const params = status ? { status } : {};
  const response = await api.get<DownloadTask[]>('/downloads', { params });
  return response.data;
};

export const getDownload = async (downloadId: number): Promise<DownloadTask> => {
  const response = await api.get<DownloadTask>(`/downloads/${downloadId}`);
  return response.data;
};

export const pauseDownload = async (downloadId: number): Promise<void> => {
  await api.post(`/downloads/${downloadId}/pause`);
};

export const resumeDownload = async (downloadId: number): Promise<void> => {
  await api.post(`/downloads/${downloadId}/resume`);
};

export const cancelDownload = async (downloadId: number): Promise<void> => {
  await api.delete(`/downloads/${downloadId}`);
};

// ============================================
// LIBRARY
// ============================================

export const getLibrary = async (params?: {
  skip?: number;
  limit?: number;
  search?: string;
}): Promise<Novel[]> => {
  const response = await api.get<Novel[]>('/library', { params });
  return response.data;
};

export const getNovel = async (novelId: number): Promise<Novel> => {
  const response = await api.get<Novel>(`/library/${novelId}`);
  return response.data;
};

export const deleteNovel = async (novelId: number): Promise<void> => {
  await api.delete(`/library/${novelId}`);
};

// ============================================
// FAVORITES
// ============================================

export const getFavorites = async (): Promise<Novel[]> => {
  const response = await api.get<Novel[]>('/favorites');
  return response.data;
};

export const addFavorite = async (novelId: number): Promise<void> => {
  await api.post(`/favorites/${novelId}`);
};

export const removeFavorite = async (novelId: number): Promise<void> => {
  await api.delete(`/favorites/${novelId}`);
};

// ============================================
// HISTORY
// ============================================

export const getHistory = async (params?: {
  skip?: number;
  limit?: number;
}): Promise<Novel[]> => {
  const response = await api.get<Novel[]>('/history', { params });
  return response.data;
};