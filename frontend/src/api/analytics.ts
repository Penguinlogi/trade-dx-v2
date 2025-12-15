/**
 * 分析・集計API
 */
import { axiosInstance } from './axios';
import type {
  AnalyticsSummaryResponse,
  TrendsResponse,
  CustomerRevenueResponse,
  AnalyticsFilters,
} from '../types/analytics';

const API_BASE = '/api/analytics';

/**
 * 集計サマリーを取得
 */
export const getAnalyticsSummary = async (
  filters?: AnalyticsFilters
): Promise<AnalyticsSummaryResponse> => {
  const response = await axiosInstance.get<AnalyticsSummaryResponse>(
    `${API_BASE}/summary`,
    { params: filters }
  );
  return response.data;
};

/**
 * 月次トレンドを取得
 */
export const getAnalyticsTrends = async (
  periodMonths: number = 12
): Promise<TrendsResponse> => {
  const response = await axiosInstance.get<TrendsResponse>(
    `${API_BASE}/trends`,
    { params: { period_months: periodMonths } }
  );
  return response.data;
};

/**
 * 顧客別売上TOP取得
 */
export const getAnalyticsByCustomer = async (
  limit: number = 10
): Promise<CustomerRevenueResponse> => {
  const response = await axiosInstance.get<CustomerRevenueResponse>(
    `${API_BASE}/by-customer`,
    { params: { limit } }
  );
  return response.data;
};





