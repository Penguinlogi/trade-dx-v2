/**
 * 認証API
 */
import { axiosInstance } from './axios';
import { LoginRequest, LoginResponse, User, Token } from '../types/auth';

/**
 * ログイン
 */
export const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
  // OAuth2PasswordRequestForm形式に変換
  const formData = new FormData();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  const response = await axiosInstance.post<LoginResponse>('/api/auth/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * ログアウト
 */
export const logout = async (): Promise<void> => {
  await axiosInstance.post('/api/auth/logout');
};

/**
 * 現在のユーザー情報を取得
 */
export const getCurrentUser = async (): Promise<User> => {
  const response = await axiosInstance.get<User>('/api/auth/me');
  return response.data;
};

/**
 * トークンをリフレッシュ
 */
export const refreshToken = async (): Promise<Token> => {
  const response = await axiosInstance.post<Token>('/api/auth/refresh');
  return response.data;
};


