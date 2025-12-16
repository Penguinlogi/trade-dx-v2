/**
 * ダッシュボードページ
 */
import React, { useEffect, useState, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  AppBar,
  Toolbar,
  IconButton,
  CircularProgress,
  Alert,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import { Logout, Dashboard as DashboardIcon, Refresh } from '@mui/icons-material';
import {
  SummaryCards,
  StatusDistributionChart,
  MonthlyTrendChart,
  TopCustomersTable,
} from '../components/Dashboard';
import { ServerStatusIndicator } from '../components/ServerStatus';
import { RealtimeNotification } from '../components/RealtimeNotification';
import {
  getAnalyticsSummary,
  getAnalyticsTrends,
  getAnalyticsByCustomer,
} from '../api/analytics';
import type {
  AnalyticsSummaryResponse,
  TrendsResponse,
  CustomerRevenueResponse,
} from '../types/analytics';

/**
 * エラーメッセージを取得するヘルパー関数
 */
const getErrorMessage = (err: any): string => {
  if (err.response?.data?.detail) {
    return err.response.data.detail;
  }
  if (err.response?.status) {
    if (err.response.status === 401) {
      return '認証エラー: 再度ログインしてください';
    }
    if (err.response.status === 403) {
      return '権限エラー: アクセス権限がありません';
    }
    if (err.response.status === 404) {
      return 'エンドポイントが見つかりません';
    }
    if (err.response.status >= 500) {
      return `サーバーエラー (${err.response.status}): しばらく待ってから再度お試しください`;
    }
    return `HTTPエラー (${err.response.status})`;
  }
  if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
    return 'タイムアウト: サーバーの応答が遅い可能性があります';
  }
  if (err.code === 'ERR_NETWORK' || err.message?.includes('Network Error')) {
    return 'ネットワークエラー: サーバーに接続できません';
  }
  if (err.message) {
    return err.message;
  }
  return '不明なエラーが発生しました';
};

export const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  // 状態管理
  const [summaryData, setSummaryData] = useState<AnalyticsSummaryResponse | null>(null);
  const [trendsData, setTrendsData] = useState<TrendsResponse | null>(null);
  const [customersData, setCustomersData] = useState<CustomerRevenueResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [trendsLoading, setTrendsLoading] = useState(false);
  const [customersLoading, setCustomersLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [periodMonths, setPeriodMonths] = useState(12);
  const [topCustomersLimit, setTopCustomersLimit] = useState(10);

  // スクロール位置を保存するためのref
  const scrollPositionRef = useRef<number>(0);

  // 初回データ取得
  const fetchInitialData = async () => {
    try {
      setLoading(true);
      setError(null);

      // 各API呼び出しを個別に処理して、エラーの詳細を把握できるようにする
      const results = await Promise.allSettled([
        getAnalyticsSummary().catch(err => ({ error: 'summary', err })),
        getAnalyticsTrends(periodMonths).catch(err => ({ error: 'trends', err })),
        getAnalyticsByCustomer(topCustomersLimit).catch(err => ({ error: 'customers', err })),
      ]);

      const errors: string[] = [];

      // サマリーデータの処理
      if (results[0].status === 'fulfilled' && !('error' in results[0].value)) {
        setSummaryData(results[0].value);
      } else {
        const errorData = results[0].status === 'fulfilled' ? results[0].value : results[0].reason;
        const err = 'error' in errorData ? errorData.err : errorData;
        console.error('サマリーデータ取得エラー:', err);
        errors.push(`サマリー: ${getErrorMessage(err)}`);
      }

      // トレンドデータの処理
      if (results[1].status === 'fulfilled' && !('error' in results[1].value)) {
        setTrendsData(results[1].value);
      } else {
        const errorData = results[1].status === 'fulfilled' ? results[1].value : results[1].reason;
        const err = 'error' in errorData ? errorData.err : errorData;
        console.error('トレンドデータ取得エラー:', err);
        errors.push(`トレンド: ${getErrorMessage(err)}`);
      }

      // 顧客データの処理
      if (results[2].status === 'fulfilled' && !('error' in results[2].value)) {
        setCustomersData(results[2].value);
      } else {
        const errorData = results[2].status === 'fulfilled' ? results[2].value : results[2].reason;
        const err = 'error' in errorData ? errorData.err : errorData;
        console.error('顧客データ取得エラー:', err);
        errors.push(`顧客別売上: ${getErrorMessage(err)}`);
      }

      // エラーがある場合は表示
      if (errors.length > 0) {
        setError(`データの取得に失敗しました: ${errors.join(', ')}`);
      }
    } catch (err: any) {
      console.error('データ取得エラー:', err);
      setError(`データの取得に失敗しました: ${getErrorMessage(err)}`);
    } finally {
      setLoading(false);
    }
  };

  // トレンドデータのみ再取得
  const fetchTrendsData = async (months: number) => {
    // スクロール位置を保存
    scrollPositionRef.current = window.scrollY;

    try {
      setTrendsLoading(true);
      const trends = await getAnalyticsTrends(months);
      setTrendsData(trends);
    } catch (err: any) {
      console.error('トレンドデータ取得エラー:', err);
      setError(`トレンドデータの取得に失敗しました: ${getErrorMessage(err)}`);
    } finally {
      setTrendsLoading(false);
      // スクロール位置を復元
      setTimeout(() => {
        window.scrollTo(0, scrollPositionRef.current);
      }, 0);
    }
  };

  // 顧客データのみ再取得
  const fetchCustomersData = async (limit: number) => {
    // スクロール位置を保存
    scrollPositionRef.current = window.scrollY;

    try {
      setCustomersLoading(true);
      const customers = await getAnalyticsByCustomer(limit);
      setCustomersData(customers);
    } catch (err: any) {
      console.error('顧客データ取得エラー:', err);
      setError(`顧客別売上データの取得に失敗しました: ${getErrorMessage(err)}`);
    } finally {
      setCustomersLoading(false);
      // スクロール位置を復元
      setTimeout(() => {
        window.scrollTo(0, scrollPositionRef.current);
      }, 0);
    }
  };

  // 全データ再取得
  const fetchAllData = async () => {
    try {
      setLoading(true);
      setError(null);

      // 各API呼び出しを個別に処理して、エラーの詳細を把握できるようにする
      const results = await Promise.allSettled([
        getAnalyticsSummary().catch(err => ({ error: 'summary', err })),
        getAnalyticsTrends(periodMonths).catch(err => ({ error: 'trends', err })),
        getAnalyticsByCustomer(topCustomersLimit).catch(err => ({ error: 'customers', err })),
      ]);

      const errors: string[] = [];

      // サマリーデータの処理
      if (results[0].status === 'fulfilled' && !('error' in results[0].value)) {
        setSummaryData(results[0].value);
      } else {
        const errorData = results[0].status === 'fulfilled' ? results[0].value : results[0].reason;
        const err = 'error' in errorData ? errorData.err : errorData;
        console.error('サマリーデータ取得エラー:', err);
        errors.push(`サマリー: ${getErrorMessage(err)}`);
      }

      // トレンドデータの処理
      if (results[1].status === 'fulfilled' && !('error' in results[1].value)) {
        setTrendsData(results[1].value);
      } else {
        const errorData = results[1].status === 'fulfilled' ? results[1].value : results[1].reason;
        const err = 'error' in errorData ? errorData.err : errorData;
        console.error('トレンドデータ取得エラー:', err);
        errors.push(`トレンド: ${getErrorMessage(err)}`);
      }

      // 顧客データの処理
      if (results[2].status === 'fulfilled' && !('error' in results[2].value)) {
        setCustomersData(results[2].value);
      } else {
        const errorData = results[2].status === 'fulfilled' ? results[2].value : results[2].reason;
        const err = 'error' in errorData ? errorData.err : errorData;
        console.error('顧客データ取得エラー:', err);
        errors.push(`顧客別売上: ${getErrorMessage(err)}`);
      }

      // エラーがある場合は表示
      if (errors.length > 0) {
        setError(`データの取得に失敗しました: ${errors.join(', ')}`);
      }
    } catch (err: any) {
      console.error('データ取得エラー:', err);
      setError(`データの取得に失敗しました: ${getErrorMessage(err)}`);
    } finally {
      setLoading(false);
    }
  };

  // 初回ロード時のみ全データ取得
  useEffect(() => {
    fetchInitialData();
  }, []);

  // 期間変更時はトレンドデータのみ再取得
  useEffect(() => {
    if (summaryData) {
      fetchTrendsData(periodMonths);
    }
  }, [periodMonths]);

  // 表示件数変更時は顧客データのみ再取得
  useEffect(() => {
    if (summaryData) {
      fetchCustomersData(topCustomersLimit);
    }
  }, [topCustomersLimit]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleRefresh = () => {
    fetchAllData();
  };

  // 期間変更ハンドラー
  const handlePeriodChange = (months: number) => {
    setPeriodMonths(months);
  };

  // 表示件数変更ハンドラー
  const handleLimitChange = (limit: number) => {
    setTopCustomersLimit(limit);
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.100' }}>
      {/* ヘッダー */}
      <AppBar position="static">
        <Toolbar>
          <DashboardIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            貿易DX管理システム
          </Typography>
          <IconButton color="inherit" onClick={handleRefresh} title="データ更新">
            <Refresh />
          </IconButton>
          <Typography variant="body2" sx={{ mx: 2 }}>
            {user?.full_name || user?.username}
          </Typography>
          <ServerStatusIndicator compact />
          <IconButton color="inherit" onClick={handleLogout} title="ログアウト">
            <Logout />
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* リアルタイム通知 */}
      <RealtimeNotification />

      {/* メインコンテンツ */}
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4" component="h1">
            ダッシュボード
          </Typography>
        </Box>

        {/* エラー表示 */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* ローディング表示 */}
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight={400}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            {/* サマリーカード */}
            {summaryData && (
              <Box mb={4}>
                <SummaryCards summary={summaryData.summary} />
              </Box>
            )}

            {/* 機能カード（簡易版） */}
            <Box mb={4}>
              <Typography variant="h6" gutterBottom>
                クイックアクセス
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        案件管理
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        案件の登録・編集・検索
                      </Typography>
                      <Button variant="contained" onClick={() => navigate('/cases')}>
                        案件一覧へ
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        顧客マスタ
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        顧客情報の管理
                      </Typography>
                      <Button variant="contained" onClick={() => navigate('/customers')}>
                        顧客一覧へ
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        商品マスタ
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        商品情報の管理
                      </Typography>
                      <Button variant="contained" onClick={() => navigate('/products')}>
                        商品一覧へ
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        ドキュメント履歴
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Invoice・Packing Listの履歴
                      </Typography>
                      <Button variant="contained" onClick={() => navigate('/documents')}>
                        履歴を見る
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        変更履歴
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        案件の変更履歴を確認
                      </Typography>
                      <Button variant="contained" onClick={() => navigate('/change-history')}>
                        履歴を見る
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>

            {/* グリッドレイアウト */}
            <Grid container spacing={3}>
              {/* ステータス分布 */}
              <Grid item xs={12} md={6}>
                {summaryData && (
                  <StatusDistributionChart
                    distribution={summaryData.status_distribution}
                  />
                )}
              </Grid>

              {/* 顧客別売上TOP */}
              <Grid item xs={12} md={6}>
                <Box>
                  <Box display="flex" justifyContent="flex-end" mb={1}>
                    <FormControl size="small" sx={{ minWidth: 120 }}>
                      <InputLabel>表示件数</InputLabel>
                      <Select
                        value={topCustomersLimit}
                        label="表示件数"
                        onChange={(e) => handleLimitChange(Number(e.target.value))}
                        disabled={customersLoading}
                      >
                        <MenuItem value={5}>TOP 5</MenuItem>
                        <MenuItem value={10}>TOP 10</MenuItem>
                        <MenuItem value={20}>TOP 20</MenuItem>
                      </Select>
                    </FormControl>
                  </Box>
                  {customersLoading ? (
                    <Card>
                      <CardContent>
                        <Box display="flex" justifyContent="center" alignItems="center" minHeight={300}>
                          <CircularProgress />
                        </Box>
                      </CardContent>
                    </Card>
                  ) : customersData ? (
                    <TopCustomersTable
                      customers={customersData.top_customers}
                      limit={topCustomersLimit}
                    />
                  ) : null}
                </Box>
              </Grid>

              {/* 月次トレンド */}
              <Grid item xs={12}>
                <Box>
                  <Box display="flex" justifyContent="flex-end" mb={1}>
                    <FormControl size="small" sx={{ minWidth: 120 }}>
                      <InputLabel>期間</InputLabel>
                      <Select
                        value={periodMonths}
                        label="期間"
                        onChange={(e) => handlePeriodChange(Number(e.target.value))}
                        disabled={trendsLoading}
                      >
                        <MenuItem value={6}>6ヶ月</MenuItem>
                        <MenuItem value={12}>12ヶ月</MenuItem>
                        <MenuItem value={24}>24ヶ月</MenuItem>
                      </Select>
                    </FormControl>
                  </Box>
                  {trendsLoading ? (
                    <Card>
                      <CardContent>
                        <Box display="flex" justifyContent="center" alignItems="center" minHeight={300}>
                          <CircularProgress />
                        </Box>
                      </CardContent>
                    </Card>
                  ) : trendsData ? (
                    <MonthlyTrendChart
                      trends={trendsData.trends}
                      periodMonths={periodMonths}
                    />
                  ) : null}
                </Box>
              </Grid>
            </Grid>
          </>
        )}
      </Container>
    </Box>
  );
};
