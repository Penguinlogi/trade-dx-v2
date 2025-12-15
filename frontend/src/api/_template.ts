/**
 * [機能名] API
 *
 * このテンプレートをコピーして新しいAPIファイルを作成してください
 *
 * 使用方法:
 * 1. このファイルをコピーして新しいファイル名に変更
 * 2. [機能名]、YourDataType、your-endpoint を実際の名前に置換
 * 3. 必要なメソッドだけ残して、不要なメソッドは削除
 * 4. 型定義を実際のデータ構造に合わせて修正
 */

import { axiosInstance } from './axios';

// =============================================================================
// 型定義
// =============================================================================

/**
 * [説明] データ型
 */
export interface YourDataType {
  /** ID */
  id: number;
  /** 名前 */
  name: string;
  /** 説明 */
  description?: string;
  /** 作成日時 */
  created_at: string;
  /** 更新日時 */
  updated_at: string;
}

/**
 * [説明] 作成リクエスト
 */
export interface YourDataCreateRequest {
  name: string;
  description?: string;
}

/**
 * [説明] 更新リクエスト
 */
export interface YourDataUpdateRequest {
  name?: string;
  description?: string;
}

/**
 * [説明] 一覧レスポンス
 */
export interface YourDataListResponse {
  items: YourDataType[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

/**
 * [説明] 検索パラメータ
 */
export interface YourDataSearchParams {
  page?: number;
  page_size?: number;
  search?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

// =============================================================================
// API関数
// =============================================================================

/**
 * [説明]一覧を取得
 *
 * @param params - 検索パラメータ
 * @returns [説明]一覧
 *
 * @example
 * ```typescript
 * const response = await getYourDataList({ page: 1, page_size: 20 });
 * console.log(response.items);
 * ```
 */
export const getYourDataList = async (
  params?: YourDataSearchParams
): Promise<YourDataListResponse> => {
  const response = await axiosInstance.get<YourDataListResponse>(
    '/api/your-endpoint', // または ENDPOINTS.YOUR_ENDPOINT.LIST
    { params }
  );
  return response.data;
};

/**
 * [説明]詳細を取得
 *
 * @param id - データID
 * @returns [説明]詳細
 *
 * @example
 * ```typescript
 * const item = await getYourData(1);
 * console.log(item.name);
 * ```
 */
export const getYourData = async (id: number): Promise<YourDataType> => {
  const response = await axiosInstance.get<YourDataType>(
    `/api/your-endpoint/${id}` // または ENDPOINTS.YOUR_ENDPOINT.DETAIL(id)
  );
  return response.data;
};

/**
 * [説明]を作成
 *
 * @param data - 作成データ
 * @returns 作成された[説明]
 *
 * @example
 * ```typescript
 * const newItem = await createYourData({
 *   name: 'Example',
 *   description: 'This is an example'
 * });
 * ```
 */
export const createYourData = async (
  data: YourDataCreateRequest
): Promise<YourDataType> => {
  const response = await axiosInstance.post<YourDataType>(
    '/api/your-endpoint', // または ENDPOINTS.YOUR_ENDPOINT.CREATE
    data
  );
  return response.data;
};

/**
 * [説明]を更新
 *
 * @param id - データID
 * @param data - 更新データ
 * @returns 更新された[説明]
 *
 * @example
 * ```typescript
 * const updatedItem = await updateYourData(1, {
 *   name: 'Updated Name'
 * });
 * ```
 */
export const updateYourData = async (
  id: number,
  data: YourDataUpdateRequest
): Promise<YourDataType> => {
  const response = await axiosInstance.put<YourDataType>(
    `/api/your-endpoint/${id}`, // または ENDPOINTS.YOUR_ENDPOINT.UPDATE(id)
    data
  );
  return response.data;
};

/**
 * [説明]を削除
 *
 * @param id - データID
 *
 * @example
 * ```typescript
 * await deleteYourData(1);
 * console.log('Deleted successfully');
 * ```
 */
export const deleteYourData = async (id: number): Promise<void> => {
  await axiosInstance.delete(
    `/api/your-endpoint/${id}` // または ENDPOINTS.YOUR_ENDPOINT.DELETE(id)
  );
};

// =============================================================================
// 補助関数（必要に応じて）
// =============================================================================

/**
 * [説明]を検索（オプション）
 *
 * @param keyword - 検索キーワード
 * @returns 検索結果
 */
export const searchYourData = async (
  keyword: string
): Promise<YourDataType[]> => {
  const response = await getYourDataList({
    search: keyword,
    page_size: 100,
  });
  return response.items;
};

/**
 * [説明]が存在するか確認（オプション）
 *
 * @param id - データID
 * @returns 存在する場合true
 */
export const existsYourData = async (id: number): Promise<boolean> => {
  try {
    await getYourData(id);
    return true;
  } catch {
    return false;
  }
};

// =============================================================================
// 注意事項
// =============================================================================

/*
 * このテンプレートの使用方法:
 *
 * 1. ファイル名を変更
 *    _template.ts → yourFeature.ts
 *
 * 2. 以下を一括置換
 *    YourDataType → 実際の型名（例: Product, Customer）
 *    YourData → 実際の名前（例: Product, Customer）
 *    your-endpoint → 実際のエンドポイント（例: products, customers）
 *    [説明] → 実際の説明（例: 商品, 顧客）
 *    [機能名] → 実際の機能名（例: 商品マスタ, 顧客管理）
 *
 * 3. 不要なメソッドを削除
 *    例: 読み取り専用APIの場合、create/update/deleteを削除
 *
 * 4. 必要に応じてメソッドを追加
 *    例: 特殊な検索、集計、バッチ処理など
 *
 * 5. エラーハンドリングを追加（必要に応じて）
 *    try-catch でエラーをキャッチし、適切に処理
 *
 * 6. JSDocコメントを充実させる
 *    使用例、パラメータの詳細、戻り値の説明など
 */
