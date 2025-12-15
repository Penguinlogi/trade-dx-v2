/**
 * 顧客マスタの型定義
 */

export interface Customer {
  id: number;
  customer_code: string;
  customer_name: string;
  customer_name_en: string | null;
  address: string | null;
  address_en: string | null;
  phone: string | null;
  contact_person: string | null;
  email: string | null;
  payment_terms: string | null;
  notes: string | null;
  is_active: number;
  created_at: string;
  updated_at: string;
}

export interface CustomerCreate {
  customer_code: string;
  customer_name: string;
  customer_name_en?: string | null;
  address?: string | null;
  address_en?: string | null;
  phone?: string | null;
  contact_person?: string | null;
  email?: string | null;
  payment_terms?: string | null;
  notes?: string | null;
  is_active?: number;
}

export interface CustomerUpdate {
  customer_code?: string;
  customer_name?: string;
  customer_name_en?: string | null;
  address?: string | null;
  address_en?: string | null;
  phone?: string | null;
  contact_person?: string | null;
  email?: string | null;
  payment_terms?: string | null;
  notes?: string | null;
  is_active?: number;
}

export interface CustomerListResponse {
  total: number;
  items: Customer[];
  page: number;
  page_size: number;
  total_pages: number;
}

export interface CustomerFilters {
  search?: string;
  is_active?: number;
  page?: number;
  page_size?: number;
}






