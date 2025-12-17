/**
 * 分析・集計の型定義
 */

/**
 * サマリーデータ
 */
export interface SummaryData {
  total_cases: number;
  active_cases: number;
  completed_cases: number;
  total_customers: number;
  total_products: number;
  this_month_cases: number;
  this_month_revenue: number;
  last_month_revenue: number;
}

/**
 * 案件ステータス分布
 */
export interface CaseStatusDistribution {
  status: string;
  count: number;
  percentage: number;
}

/**
 * 集計サマリーレスポンス
 */
export interface AnalyticsSummaryResponse {
  summary: SummaryData;
  status_distribution: CaseStatusDistribution[];
}

/**
 * 月次トレンドデータ
 */
export interface MonthlyTrend {
  year_month: string;
  case_count: number;
  revenue: number;
}

/**
 * トレンドレスポンス
 */
export interface TrendsResponse {
  trends: MonthlyTrend[];
  period_months: number;
}

/**
 * 顧客別売上
 */
export interface CustomerRevenue {
  customer_id: number;
  customer_code: string;
  customer_name: string;
  case_count: number;
  total_revenue: number;
}

/**
 * 顧客別売上レスポンス
 */
export interface CustomerRevenueResponse {
  top_customers: CustomerRevenue[];
  limit: number;
}

/**
 * 分析フィルター
 */
export interface AnalyticsFilters {
  start_date?: string;
  end_date?: string;
  customer_id?: number;
  status?: string;
}







