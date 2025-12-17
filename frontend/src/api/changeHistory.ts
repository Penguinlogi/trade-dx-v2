/**
 * 変更履歴API
 */
import { axiosInstance } from './axios';
import type {
  ChangeHistory,
  ChangeHistoryListResponse,
  ChangeHistorySearchParams,
} from '../types/changeHistory';

const API_BASE = '/api/change-history';

/**
 * 変更履歴一覧を取得
 */
export const getChangeHistory = async (
  params?: ChangeHistorySearchParams
): Promise<ChangeHistoryListResponse> => {
  const response = await axiosInstance.get<ChangeHistoryListResponse>(API_BASE, { params });
  return response.data;
};

/**
 * 変更履歴詳細を取得
 */
export const getChangeHistoryDetail = async (historyId: number): Promise<ChangeHistory> => {
  const response = await axiosInstance.get<ChangeHistory>(`${API_BASE}/${historyId}`);
  return response.data;
};

/**
 * 特定案件の変更履歴を取得
 */
export const getCaseChangeHistory = async (
  caseId: number,
  params?: { page?: number; page_size?: number }
): Promise<ChangeHistoryListResponse> => {
  const response = await axiosInstance.get<ChangeHistoryListResponse>(
    `${API_BASE}/case/${caseId}/history`,
    { params }
  );
  return response.data;
};








