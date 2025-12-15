/**
 * 商品マスタ API クライアント
 */
import { axiosInstance } from './axios';
import {
  Product,
  ProductCreate,
  ProductUpdate,
  ProductListResponse,
  ProductFilters,
} from '../types/product';

/**
 * 商品マスタ一覧取得
 */
export const getProducts = async (
  filters?: ProductFilters
): Promise<ProductListResponse> => {
  const params: Record<string, any> = {
    skip: ((filters?.page || 1) - 1) * (filters?.page_size || 50),
    limit: filters?.page_size || 50,
  };

  if (filters?.search) {
    params.search = filters.search;
  }
  if (filters?.category) {
    params.category = filters.category;
  }
  if (filters?.is_active !== undefined) {
    params.is_active = filters.is_active;
  }

  const response = await axiosInstance.get<ProductListResponse>('/api/products/', {
    params,
  });
  return response.data;
};

/**
 * 商品マスタ詳細取得
 */
export const getProduct = async (id: number): Promise<Product> => {
  const response = await axiosInstance.get<Product>(`/api/products/${id}`);
  return response.data;
};

/**
 * 商品マスタ新規作成
 */
export const createProduct = async (data: ProductCreate): Promise<Product> => {
  const response = await axiosInstance.post<Product>('/api/products/', data);
  return response.data;
};

/**
 * 商品マスタ更新
 */
export const updateProduct = async (
  id: number,
  data: ProductUpdate
): Promise<Product> => {
  const response = await axiosInstance.put<Product>(`/api/products/${id}`, data);
  return response.data;
};

/**
 * 商品マスタ削除（論理削除）
 */
export const deleteProduct = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/api/products/${id}`);
};

/**
 * 商品マスタオートコンプリート
 */
export const autocompleteProducts = async (
  query: string,
  limit?: number
): Promise<Product[]> => {
  const response = await axiosInstance.get<Product[]>('/api/products/autocomplete/', {
    params: { q: query, limit: limit || 10 },
  });
  return response.data;
};

/**
 * カテゴリ一覧取得
 */
export const getCategories = async (): Promise<string[]> => {
  const response = await axiosInstance.get<string[]>('/api/products/categories/');
  return response.data;
};


