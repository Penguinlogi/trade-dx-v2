/**
 * 案件API
 */
import { axiosInstance } from './axios';
import type {
  Case,
  CaseListResponse,
  CaseCreateRequest,
  CaseUpdateRequest,
  CaseSearchParams,
} from '../types/case';

const API_BASE = '/api/cases';

/**
 * 案件一覧を取得
 */
export const getCases = async (params?: CaseSearchParams): Promise<CaseListResponse> => {
  const response = await axiosInstance.get<CaseListResponse>(API_BASE, { params });
  return response.data;
};

/**
 * 案件詳細を取得
 */
export const getCase = async (caseId: number): Promise<Case> => {
  const response = await axiosInstance.get<Case>(`${API_BASE}/${caseId}`);
  return response.data;
};

/**
 * 案件を作成
 */
export const createCase = async (data: CaseCreateRequest): Promise<Case> => {
  const response = await axiosInstance.post<Case>(API_BASE, data);
  return response.data;
};

/**
 * 案件を更新
 */
export const updateCase = async (caseId: number, data: CaseUpdateRequest): Promise<Case> => {
  const response = await axiosInstance.put<Case>(`${API_BASE}/${caseId}`, data);
  return response.data;
};

/**
 * 案件を削除
 */
export const deleteCase = async (caseId: number): Promise<void> => {
  await axiosInstance.delete(`${API_BASE}/${caseId}`);
};

