/**
 * ログインページ
 */
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Box,
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  InputAdornment,
  IconButton,
} from '@mui/material';
import { Visibility, VisibilityOff, Login as LoginIcon } from '@mui/icons-material';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // リダイレクト先（ログイン前にアクセスしようとしたページ）
  const from = (location.state as any)?.from?.pathname || '/';

  /**
   * ログイン処理
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login({ username, password });
      // ログイン成功後、少し待ってからナビゲーション（状態更新を確実にするため）
      setTimeout(() => {
        navigate(from, { replace: true });
      }, 100);
    } catch (err: any) {
      setError(err.message || 'ログインに失敗しました');
      setIsLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={10}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            borderRadius: 2,
          }}
        >
          {/* ロゴ・タイトル */}
          <Box
            sx={{
              width: 60,
              height: 60,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mb: 2,
            }}
          >
            <LoginIcon sx={{ fontSize: 30, color: 'white' }} />
          </Box>

          <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
            貿易DX管理システム
          </Typography>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            ログインして続行してください
          </Typography>

          {/* エラーメッセージ */}
          {error && (
            <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* ログインフォーム */}
          <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
            <TextField
              fullWidth
              label="ユーザー名"
              variant="outlined"
              margin="normal"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoFocus
              disabled={isLoading}
            />

            <TextField
              fullWidth
              label="パスワード"
              type={showPassword ? 'text' : 'password'}
              variant="outlined"
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={isLoading}
              sx={{
                mt: 3,
                mb: 2,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)',
                },
              }}
            >
              {isLoading ? 'ログイン中...' : 'ログイン'}
            </Button>
          </Box>

          {/* デモ用の情報（開発環境のみ） */}
          {import.meta.env.DEV && (
            <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1, width: '100%' }}>
              <Typography variant="caption" display="block" gutterBottom>
                <strong>デモ用アカウント:</strong>
              </Typography>
              <Typography variant="caption" display="block">
                ユーザー名: admin / パスワード: admin123
              </Typography>
              <Typography variant="caption" display="block">
                ユーザー名: yamada / パスワード: yamada123
              </Typography>
              <Typography variant="caption" display="block">
                ユーザー名: suzuki / パスワード: suzuki123
              </Typography>
              <Typography variant="caption" display="block" sx={{ mt: 1, color: 'warning.main' }}>
                ※ データベースにユーザーが存在しない場合は、シードデータを投入してください
              </Typography>
            </Box>
          )}
        </Paper>
      </Container>
    </Box>
  );
};
