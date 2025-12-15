/**
 * 顧客マスタ API クライアント
 */
import { axiosInstance } from './axios';
import {
  Customer,
  CustomerCreate,
  CustomerUpdate,
  CustomerListResponse,
  CustomerFilters,
} from '../types/customer';

/**
 * 顧客マスタ一覧取得
 */
export const getCustomers = async (
  filters?: CustomerFilters
): Promise<CustomerListResponse> => {
  const params: Record<string, any> = {
    skip: ((filters?.page || 1) - 1) * (filters?.page_size || 50),
    limit: filters?.page_size || 50,
  };

  if (filters?.search) {
    params.search = filters.search;
  }
  if (filters?.is_active !== undefined) {
    params.is_active = filters.is_active;
  }

  const response = await axiosInstance.get<CustomerListResponse>('/api/customers/', {
    params,
  });
  return response.data;
};

/**
 * 顧客マスタ詳細取得
 */
export const getCustomer = async (id: number): Promise<Customer> => {
  const response = await axiosInstance.get<Customer>(`/api/customers/${id}`);
  return response.data;
};

/**
 * 顧客マスタ新規作成
 */
export const createCustomer = async (data: CustomerCreate): Promise<Customer> => {
  const response = await axiosInstance.post<Customer>('/api/customers/', data);
  return response.data;
};

/**
 * 顧客マスタ更新
 */
export const updateCustomer = async (
  id: number,
  data: CustomerUpdate
): Promise<Customer> => {
  const response = await axiosInstance.put<Customer>(`/api/customers/${id}`, data);
  return response.data;
};

/**
 * 顧客マスタ削除（論理削除）
 */
export const deleteCustomer = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/api/customers/${id}`);
};

/**
 * 顧客マスタオートコンプリート
 */
export const autocompleteCustomers = async (
  query: string,
  limit?: number
): Promise<Customer[]> => {
  const response = await axiosInstance.get<Customer[]>('/api/customers/autocomplete/', {
    params: { q: query, limit: limit || 10 },
  });
  return response.data;
};


