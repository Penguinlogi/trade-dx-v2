/**
 * バックアップAPI
 */
import { axiosInstance } from './axios';
import type {
  Backup,
  BackupListResponse,
  BackupCreateRequest,
  BackupSearchParams,
} from '../types/backup';

const API_BASE = '/api/backups';

/**
 * バックアップ一覧を取得
 */
export const getBackups = async (params?: BackupSearchParams): Promise<BackupListResponse> => {
  const response = await axiosInstance.get<BackupListResponse>(API_BASE, { params });
  return response.data;
};

/**
 * バックアップ詳細を取得
 */
export const getBackup = async (backupId: number): Promise<Backup> => {
  const response = await axiosInstance.get<Backup>(`${API_BASE}/${backupId}`);
  return response.data;
};

/**
 * バックアップを作成
 */
export const createBackup = async (data: BackupCreateRequest): Promise<Backup> => {
  const response = await axiosInstance.post<Backup>(`${API_BASE}/create`, data);
  return response.data;
};

/**
 * バックアップから復元
 */
export const restoreBackup = async (backupId: number): Promise<{ message: string; success: boolean }> => {
  const response = await axiosInstance.post<{ message: string; success: boolean }>(
    `${API_BASE}/${backupId}/restore`
  );
  return response.data;
};

/**
 * バックアップを削除
 */
export const deleteBackup = async (backupId: number): Promise<void> => {
  await axiosInstance.delete(`${API_BASE}/${backupId}`);
};

/**
 * 古いバックアップをクリーンアップ
 */
export const cleanupBackups = async (days: number = 30): Promise<{ message: string; deleted_count: number }> => {
  const response = await axiosInstance.post<{ message: string; deleted_count: number }>(
    `${API_BASE}/cleanup`,
    null,
    { params: { days } }
  );
  return response.data;
};

/**
 * スケジュールバックアップを実行
 */
export const runScheduledBackup = async (): Promise<{ message: string; executed: boolean }> => {
  const response = await axiosInstance.post<{ message: string; executed: boolean }>(
    `${API_BASE}/run-scheduled`
  );
  return response.data;
};






