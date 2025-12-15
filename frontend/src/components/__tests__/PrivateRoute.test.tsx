/**
 * PrivateRouteコンポーネントのテスト
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { PrivateRoute } from '../PrivateRoute';

// AuthContextのモック
const mockUseAuth = vi.fn();

vi.mock('../../context/AuthContext', () => ({
  useAuth: () => mockUseAuth(),
  AuthProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

describe.skip('PrivateRoute', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // モックをリセット
    mockUseAuth.mockClear();
  });

  it('認証済みユーザーは子コンポーネントを表示する', () => {
    mockUseAuth.mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: { username: 'testuser', email: 'test@example.com' },
      login: vi.fn(),
      logout: vi.fn(),
      refreshUser: vi.fn(),
    });

    render(
      <BrowserRouter>
        <PrivateRoute>
          <div>保護されたコンテンツ</div>
        </PrivateRoute>
      </BrowserRouter>
    );

    expect(screen.getByText('保護されたコンテンツ')).toBeInTheDocument();
  });

  it('未認証ユーザーはログインページにリダイレクトされる', () => {
    mockUseAuth.mockReturnValue({
      isAuthenticated: false,
      isLoading: false,
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      refreshUser: vi.fn(),
    });

    render(
      <BrowserRouter>
        <PrivateRoute>
          <div>保護されたコンテンツ</div>
        </PrivateRoute>
      </BrowserRouter>
    );

    // Navigateコンポーネントが動作するため、保護されたコンテンツは表示されない
    expect(screen.queryByText('保護されたコンテンツ')).not.toBeInTheDocument();
  });

  it('ローディング中はローディングインジケーターを表示する', () => {
    mockUseAuth.mockReturnValue({
      isAuthenticated: false,
      isLoading: true,
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      refreshUser: vi.fn(),
    });

    render(
      <BrowserRouter>
        <PrivateRoute>
          <div>保護されたコンテンツ</div>
        </PrivateRoute>
      </BrowserRouter>
    );

    // CircularProgressが表示される（MUIのコンポーネント）
    // ローディング中は保護されたコンテンツは表示されない
    expect(screen.queryByText('保護されたコンテンツ')).not.toBeInTheDocument();
  });
});
