/**
 * 認証コンテキスト
 */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, LoginRequest } from '../types/auth';
import * as authApi from '../api/auth';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * 認証プロバイダー
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // 初回マウント時にユーザー情報を取得
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      const storedUser = localStorage.getItem('user');

      if (token && storedUser) {
        try {
          // 保存されたユーザー情報を復元
          const parsedUser = JSON.parse(storedUser);
          setUser(parsedUser);

          // サーバーから最新のユーザー情報を取得
          const currentUser = await authApi.getCurrentUser();
          setUser(currentUser);
          localStorage.setItem('user', JSON.stringify(currentUser));
        } catch (error: any) {
          // トークンが無効な場合はクリア
          console.error('認証エラー:', error);
          console.error('認証エラー詳細:', {
            message: error.message,
            response: error.response?.data,
            status: error.response?.status,
            statusText: error.response?.statusText,
          });
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          setUser(null);
        }
      }

      setIsLoading(false);
    };

    initAuth();
  }, []);

  // 自動ログアウト（トークン有効期限）
  useEffect(() => {
    if (!user) return;

    // 25分後に警告を表示（トークンは30分有効）
    const warningTimer = setTimeout(() => {
      alert('セッションがまもなく期限切れになります。再ログインしてください。');
    }, 25 * 60 * 1000);

    // 30分後に自動ログアウト
    const logoutTimer = setTimeout(async () => {
      await logout();
      alert('セッションの期限が切れました。再度ログインしてください。');
    }, 30 * 60 * 1000);

    return () => {
      clearTimeout(warningTimer);
      clearTimeout(logoutTimer);
    };
  }, [user]);

  /**
   * ログイン
   */
  const login = async (credentials: LoginRequest) => {
    try {
      const response = await authApi.login(credentials);

      // トークンとユーザー情報を保存
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
      setUser(response.user);
    } catch (error: any) {
      console.error('ログインエラー:', error);
      console.error('エラー詳細:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText,
      });

      // より詳細なエラーメッセージ
      let errorMessage = 'ログインに失敗しました';

      if (error.response) {
        // サーバーからエラーレスポンスがある場合
        errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage;
      } else if (error.request) {
        // リクエストは送信されたが、レスポンスがない場合（ネットワークエラーなど）
        errorMessage = 'サーバーに接続できません。バックエンドサーバーが起動しているか確認してください。';
      } else {
        // リクエストの設定中にエラーが発生した場合
        errorMessage = error.message || errorMessage;
      }

      throw new Error(errorMessage);
    }
  };

  /**
   * ログアウト
   */
  const logout = async () => {
    try {
      await authApi.logout();
    } catch (error) {
      console.error('ログアウトエラー:', error);
    } finally {
      // ローカルストレージをクリア
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      setUser(null);
    }
  };

  /**
   * ユーザー情報を再取得
   */
  const refreshUser = async () => {
    try {
      const currentUser = await authApi.getCurrentUser();
      setUser(currentUser);
      localStorage.setItem('user', JSON.stringify(currentUser));
    } catch (error) {
      console.error('ユーザー情報取得エラー:', error);
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * 認証コンテキストを使用するフック
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
