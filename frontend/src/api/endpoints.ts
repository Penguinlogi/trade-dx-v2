/**
 * API エンドポイント定義
 *
 * すべてのAPIパスを一元管理
 *
 * 使用方法:
 * ```typescript
 * import { ENDPOINTS } from './endpoints';
 *
 * const response = await axiosInstance.get(ENDPOINTS.CASES.LIST);
 * const user = await axiosInstance.get(ENDPOINTS.USERS.DETAIL(userId));
 * ```
 */

const API_PREFIX = '/api';

/**
 * すべてのAPIエンドポイント
 */
export const ENDPOINTS = {
  /**
   * 認証関連
   */
  AUTH: {
    /** ログイン */
    LOGIN: `${API_PREFIX}/auth/login`,
    /** ログアウト */
    LOGOUT: `${API_PREFIX}/auth/logout`,
    /** 現在のユーザー情報取得 */
    ME: `${API_PREFIX}/auth/me`,
    /** トークンリフレッシュ */
    REFRESH: `${API_PREFIX}/auth/refresh`,
  },

  /**
   * 案件管理
   */
  CASES: {
    /** 案件一覧取得 */
    LIST: `${API_PREFIX}/cases`,
    /** 案件詳細取得 */
    DETAIL: (id: number) => `${API_PREFIX}/cases/${id}`,
    /** 案件作成 */
    CREATE: `${API_PREFIX}/cases`,
    /** 案件更新 */
    UPDATE: (id: number) => `${API_PREFIX}/cases/${id}`,
    /** 案件削除 */
    DELETE: (id: number) => `${API_PREFIX}/cases/${id}`,
  },

  /**
   * 案件番号生成
   */
  CASE_NUMBERS: {
    /** 案件番号生成 */
    GENERATE: `${API_PREFIX}/case-numbers/generate`,
  },

  /**
   * 顧客マスタ
   */
  CUSTOMERS: {
    /** 顧客一覧取得 */
    LIST: `${API_PREFIX}/customers`,
    /** 顧客詳細取得 */
    DETAIL: (id: number) => `${API_PREFIX}/customers/${id}`,
    /** 顧客作成 */
    CREATE: `${API_PREFIX}/customers`,
    /** 顧客更新 */
    UPDATE: (id: number) => `${API_PREFIX}/customers/${id}`,
    /** 顧客削除 */
    DELETE: (id: number) => `${API_PREFIX}/customers/${id}`,
  },

  /**
   * 商品マスタ
   */
  PRODUCTS: {
    /** 商品一覧取得 */
    LIST: `${API_PREFIX}/products`,
    /** 商品詳細取得 */
    DETAIL: (id: number) => `${API_PREFIX}/products/${id}`,
    /** 商品作成 */
    CREATE: `${API_PREFIX}/products`,
    /** 商品更新 */
    UPDATE: (id: number) => `${API_PREFIX}/products/${id}`,
    /** 商品削除 */
    DELETE: (id: number) => `${API_PREFIX}/products/${id}`,
  },

  /**
   * ドキュメント生成
   */
  DOCUMENTS: {
    /** ドキュメント一覧取得 */
    LIST: `${API_PREFIX}/documents`,
    /** Invoice生成 */
    INVOICE: `${API_PREFIX}/documents/invoice`,
    /** Packing List生成 */
    PACKING_LIST: `${API_PREFIX}/documents/packing-list`,
    /** ドキュメントダウンロード */
    DOWNLOAD: (id: number) => `${API_PREFIX}/documents/${id}/download`,
  },

  /**
   * 分析・集計
   */
  ANALYTICS: {
    /** サマリー情報取得 */
    SUMMARY: `${API_PREFIX}/analytics/summary`,
    /** トレンドデータ取得 */
    TRENDS: `${API_PREFIX}/analytics/trends`,
    /** 顧客別売上取得 */
    BY_CUSTOMER: `${API_PREFIX}/analytics/by-customer`,
  },

  /**
   * WebSocket
   */
  WEBSOCKET: {
    /** WebSocket接続 */
    WS: `${API_PREFIX}/ws`,
  },
} as const;

/**
 * エンドポイントの型
 */
export type EndpointsType = typeof ENDPOINTS;
