/**
 * 案件管理関連の型定義
 */

/**
 * 顧客情報（案件内）
 */
export interface CustomerInCase {
  id: number;
  customer_code: string;
  customer_name: string;
}

/**
 * 商品情報（案件内）
 */
export interface ProductInCase {
  id: number;
  product_code: string;
  product_name: string;
  hs_code?: string | null;
}

/**
 * 案件（詳細）
 */
export interface Case {
  id: number;
  case_number: string;
  trade_type: string;
  customer_id: number;
  supplier_name?: string | null;
  product_id: number;
  quantity: number | string;
  unit: string;
  sales_unit_price: number | string;
  purchase_unit_price: number | string;
  sales_amount?: number | string | null;
  gross_profit?: number | string | null;
  gross_profit_rate?: number | string | null;
  shipment_date?: string | null;
  status: string;
  pic: string;
  notes?: string | null;
  created_by?: number | null;
  updated_by?: number | null;
  created_at: string;
  updated_at: string;
  customer?: CustomerInCase | null;
  product?: ProductInCase | null;
}

/**
 * 案件一覧アイテム
 */
export interface CaseListItem {
  id: number;
  case_number: string;
  trade_type: string;
  customer_id: number;
  customer_name?: string | null;
  product_id: number;
  product_name?: string | null;
  quantity: number | string;
  unit: string;
  sales_amount?: number | string | null;
  gross_profit?: number | string | null;
  gross_profit_rate?: number | string | null;
  status: string;
  pic: string;
  shipment_date?: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * 案件一覧レスポンス（ページネーション付き）
 */
export interface CaseListResponse {
  items: CaseListItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

/**
 * 案件作成リクエスト
 */
export interface CaseCreateRequest {
  case_number?: string;
  trade_type: string;
  customer_id: number;
  supplier_name?: string;
  product_id: number;
  quantity: number;
  unit: string;
  sales_unit_price: number;
  purchase_unit_price: number;
  shipment_date?: string;
  status: string;
  pic: string;
  notes?: string;
}

/**
 * 案件更新リクエスト
 */
export interface CaseUpdateRequest {
  trade_type?: string;
  customer_id?: number;
  supplier_name?: string;
  product_id?: number;
  quantity?: number;
  unit?: string;
  sales_unit_price?: number;
  purchase_unit_price?: number;
  shipment_date?: string;
  status?: string;
  pic?: string;
  notes?: string;
}

/**
 * 案件検索パラメータ
 */
export interface CaseSearchParams {
  page?: number;
  page_size?: number;
  trade_type?: string;
  status?: string;
  customer_id?: number;
  product_id?: number;
  pic?: string;
  search?: string;
  shipment_date_from?: string;
  shipment_date_to?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

/**
 * 区分（輸出/輸入）
 */
export type TradeType = '輸出' | '輸入';

/**
 * ステータス
 */
export type CaseStatus = '見積中' | '受注済' | '船積済' | '完了' | 'キャンセル';

/**
 * 区分の選択肢
 */
export const TRADE_TYPES: TradeType[] = ['輸出', '輸入'];

/**
 * ステータスの選択肢
 */
export const CASE_STATUSES: CaseStatus[] = ['見積中', '受注済', '船積済', '完了', 'キャンセル'];

