/**
 * 案件番号API
 */
import { axiosInstance } from './axios';

const API_BASE = '/api/case-numbers';

export interface CaseNumberGenerateRequest {
  trade_type: string;
}

export interface CaseNumberGenerateResponse {
  case_number: string;
  year: number;
  trade_type: string;
  trade_type_code: string;
  sequence: number;
}

/**
 * 案件番号を生成
 */
export const generateCaseNumber = async (
  tradeType: string
): Promise<CaseNumberGenerateResponse> => {
  const response = await axiosInstance.post<CaseNumberGenerateResponse>(
    `${API_BASE}/generate`,
    { trade_type: tradeType }
  );
  return response.data;
};

/**
 * 現在の連番を取得
 */
export const getCurrentSequence = async (tradeType: string): Promise<any> => {
  const response = await axiosInstance.get(`${API_BASE}/current/${tradeType}`);
  return response.data;
};

