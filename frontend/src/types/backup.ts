/**
 * バックアップの型定義
 */

export type BackupType = 'manual' | 'auto' | 'scheduled';
export type BackupStatus = 'success' | 'failed' | 'in_progress';

export interface Backup {
  id: number;
  backup_name: string;
  backup_path: string;
  backup_type: BackupType;
  file_size: number | null;
  record_count: number | null;
  status: BackupStatus;
  error_message: string | null;
  created_by: number | null;
  created_at: string;
}

export interface BackupListResponse {
  items: Backup[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface BackupCreateRequest {
  backup_name?: string;
  backup_type?: BackupType;
}

export interface BackupSearchParams {
  page?: number;
  page_size?: number;
  backup_type?: BackupType;
  status?: BackupStatus;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}








