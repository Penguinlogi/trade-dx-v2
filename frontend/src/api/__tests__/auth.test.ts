/**
 * 認証APIのテスト
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import * as authApi from '../auth';
import { axiosInstance } from '../axios';

// axiosのモック
vi.mock('../axios', () => ({
  axiosInstance: {
    post: vi.fn(),
    get: vi.fn(),
  },
}));

describe('認証API', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('ログインが成功する', async () => {
    const mockResponse = {
      data: {
        access_token: 'test_token',
        token_type: 'bearer',
        user: {
          id: 1,
          username: 'testuser',
          email: 'test@example.com',
          full_name: 'テストユーザー',
          is_active: true,
          is_superuser: false,
        },
      },
    };

    vi.mocked(axiosInstance.post).mockResolvedValue(mockResponse);

    const result = await authApi.login({
      username: 'testuser',
      password: 'password',
    });

    expect(result).toEqual(mockResponse.data);
    expect(axiosInstance.post).toHaveBeenCalledWith(
      '/api/auth/login',
      expect.any(FormData),
      expect.objectContaining({
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
    );
  });

  it('現在のユーザー情報を取得する', async () => {
    const mockUser = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      full_name: 'テストユーザー',
      is_active: true,
      is_superuser: false,
    };

    vi.mocked(axiosInstance.get).mockResolvedValue({ data: mockUser });

    const result = await authApi.getCurrentUser();

    expect(result).toEqual(mockUser);
    expect(axiosInstance.get).toHaveBeenCalledWith('/api/auth/me');
  });

  it('ログアウトが成功する', async () => {
    vi.mocked(axiosInstance.post).mockResolvedValue({ data: {} });

    await authApi.logout();

    expect(axiosInstance.post).toHaveBeenCalledWith('/api/auth/logout');
  });
});
