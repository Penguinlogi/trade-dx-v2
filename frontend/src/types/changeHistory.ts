/**
 * 変更履歴の型定義
 */

export type ChangeType = 'CREATE' | 'UPDATE' | 'DELETE';

export interface ChangeHistory {
  id: number;
  case_id: number;
  changed_by: number | null;
  change_type: ChangeType;
  field_name: string | null;
  old_value: string | null;
  new_value: string | null;
  changes_json: Record<string, { old: string | null; new: string | null }> | null;
  notes: string | null;
  changed_at: string;
}

export interface ChangeHistoryListItem {
  id: number;
  case_id: number;
  case_number: string | null;
  changed_by: number | null;
  changed_by_name: string | null;
  change_type: ChangeType;
  field_name: string | null;
  old_value: string | null;
  new_value: string | null;
  changes_json: Record<string, { old: string | null; new: string | null }> | null;
  notes: string | null;
  changed_at: string;
}

export interface ChangeHistoryListResponse {
  items: ChangeHistoryListItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ChangeHistorySearchParams {
  page?: number;
  page_size?: number;
  case_id?: number;
  case_number?: string;
  change_type?: ChangeType;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}
