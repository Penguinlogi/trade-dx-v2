/**
 * 商品マスタの型定義
 */

export interface Product {
  id: number;
  product_code: string;
  product_name: string;
  product_name_en: string | null;
  hs_code: string | null;
  unit: string | null;
  standard_price: number | null;
  category: string | null;
  specification: string | null;
  notes: string | null;
  is_active: number;
  created_at: string;
  updated_at: string;
}

export interface ProductCreate {
  product_code: string;
  product_name: string;
  product_name_en?: string | null;
  hs_code?: string | null;
  unit?: string | null;
  standard_price?: number | null;
  category?: string | null;
  specification?: string | null;
  notes?: string | null;
  is_active?: number;
}

export interface ProductUpdate {
  product_code?: string;
  product_name?: string;
  product_name_en?: string | null;
  hs_code?: string | null;
  unit?: string | null;
  standard_price?: number | null;
  category?: string | null;
  specification?: string | null;
  notes?: string | null;
  is_active?: number;
}

export interface ProductListResponse {
  total: number;
  items: Product[];
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ProductFilters {
  search?: string;
  category?: string;
  is_active?: number;
  page?: number;
  page_size?: number;
}






