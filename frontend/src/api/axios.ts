/**
 * Axios設定
 */
import axios from 'axios';

// APIベースURL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Axiosインスタンスの作成
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30秒のタイムアウト（Render無料プランのスリープからの復帰を考慮）
});

// リクエストインターセプター（トークンの自動付与）
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// レスポンスインターセプター（エラーハンドリング）
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // 401エラー（未認証）の場合
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // トークンをクリアしてログインページへリダイレクト
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

export { axiosInstance };
