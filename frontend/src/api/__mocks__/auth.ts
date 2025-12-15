/**
 * 認証APIのモック
 */
import { LoginRequest, LoginResponse, User, Token } from '../../types/auth';

export const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
  // モックレスポンス
  return {
    access_token: 'mock_access_token',
    token_type: 'bearer',
    user: {
      id: 1,
      username: credentials.username,
      email: 'test@example.com',
      full_name: 'テストユーザー',
      created_at: '2025-01-01T00:00:00Z',
      updated_at: '2025-01-01T00:00:00Z',
      is_active: true,
      is_superuser: false,
    },
  };
};

export const logout = async (): Promise<void> => {
  // モック実装
};

export const getCurrentUser = async (): Promise<User> => {
  return {
    id: 1,
    username: 'testuser',
    email: 'test@example.com',
    full_name: 'テストユーザー',
    created_at: '2025-01-01T00:00:00Z',
    updated_at: '2025-01-01T00:00:00Z',
    is_active: true,
    is_superuser: false,
  };
};

export const refreshToken = async (): Promise<Token> => {
  return {
    access_token: 'new_mock_access_token',
    token_type: 'bearer',
  };
};
