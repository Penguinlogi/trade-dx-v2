/**
 * 案件一覧ページ
 */
import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Box,
  Button,
  Container,
  Typography,
  Paper,
  Grid,
  TextField,
  MenuItem,
  Pagination,
  CircularProgress,
  Alert,
  Stack,
} from '@mui/material';
import { Add as AddIcon, Search as SearchIcon, FilterList as FilterIcon } from '@mui/icons-material';
import { CaseTable } from '../components/Table/CaseTable';
import { CaseFormModal } from '../components/Modal/CaseFormModal';
import { getCases, deleteCase, getCase } from '../api/cases';
import type { CaseListItem, CaseSearchParams, Case } from '../types/case';
import { useWebSocket } from '../hooks/useWebSocket';

const TRADE_TYPES_ARRAY = ['輸出', '輸入'];
const CASE_STATUSES_ARRAY = ['見積中', '受注済', '船積済', '完了', 'キャンセル'];

/**
 * 案件一覧ページ
 */
export const CasesPage: React.FC = () => {
  // ステート
  const [cases, setCases] = useState<CaseListItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);

  // モーダル
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<'create' | 'edit'>('create');
  const [selectedCase, setSelectedCase] = useState<Case | null>(null);

  // フィルター
  const [searchParams, setSearchParams] = useState<CaseSearchParams>({
    page: 1,
    page_size: 20,
    sort_by: 'created_at',
    sort_order: 'desc',
  });

  /**
   * 案件一覧を取得
   */
  const fetchCases = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getCases(searchParams);
      setCases(response.items);
      setTotal(response.total);
      setPage(response.page);
      setTotalPages(response.total_pages);
    } catch (err) {
      setError('案件一覧の取得に失敗しました');
      console.error('Error fetching cases:', err);
    } finally {
      setLoading(false);
    }
  }, [searchParams]);

  // WebSocket接続
  const { lastMessage } = useWebSocket();
  const isUserActionRef = useRef(false);

  /**
   * 初回レンダリング時と検索パラメータ変更時に案件を取得
   */
  useEffect(() => {
    fetchCases();
  }, [searchParams]);

  /**
   * WebSocketメッセージを受信したときに案件一覧を更新
   */
  useEffect(() => {
    if (!lastMessage) {
      console.log('lastMessage is null');
      return;
    }

    console.log('lastMessageが更新されました:', lastMessage);

    // ユーザー自身の操作による更新はスキップ（重複更新を防ぐ）
    if (isUserActionRef.current) {
      console.log('ユーザー自身の操作による更新をスキップ');
      isUserActionRef.current = false;
      return;
    }

    // 案件更新通知を受信した場合、一覧を再取得
    if (lastMessage.type === 'case_updated') {
      console.log('WebSocket通知を受信: 案件一覧を更新します', lastMessage);
      fetchCases();
    } else {
      console.log('案件更新以外のメッセージ:', lastMessage.type);
    }
  }, [lastMessage, fetchCases]);

  /**
   * カスタムイベントリスナー（WebSocket更新イベント）
   */
  useEffect(() => {
    const handleWebSocketUpdate = (event: CustomEvent) => {
      const message = event.detail;
      console.log('カスタムイベントを受信: websocket:update', message);

      if (message.type === 'case_updated') {
        // ユーザー自身の操作による更新はスキップ
        if (isUserActionRef.current) {
          console.log('ユーザー自身の操作による更新をスキップ（カスタムイベント）');
          isUserActionRef.current = false;
          return;
        }

        console.log('カスタムイベントから案件一覧を更新します', message);
        fetchCases();
      }
    };

    window.addEventListener('websocket:update', handleWebSocketUpdate as EventListener);

    return () => {
      window.removeEventListener('websocket:update', handleWebSocketUpdate as EventListener);
    };
  }, [fetchCases]);

  /**
   * 案件を削除
   */
  const handleDelete = async (caseItem: CaseListItem) => {
    if (!confirm(`案件番号 ${caseItem.case_number} を削除してもよろしいですか？`)) {
      return;
    }

    try {
      isUserActionRef.current = true;
      await deleteCase(caseItem.id);
      fetchCases(); // 削除後、一覧を再取得
    } catch (err) {
      alert('案件の削除に失敗しました');
      console.error('Error deleting case:', err);
    }
  };

  /**
   * ページ変更
   */
  const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
    setSearchParams((prev) => ({ ...prev, page: value }));
  };

  /**
   * 日付値をYYYY-MM-DD形式に正規化
   */
  const normalizeDateValue = (value: string): string => {
    if (!value) return '';
    // YYYY-MM-DD形式に変換（既に正しい形式の場合はそのまま）
    const dateMatch = value.match(/(\d{4})[/-](\d{1,2})[/-](\d{1,2})/);
    if (dateMatch) {
      const [, year, month, day] = dateMatch;
      return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
    }
    return value;
  };

  /**
   * フィルターの更新
   */
  const handleFilterChange = (field: keyof CaseSearchParams, value: any) => {
    // 日付フィールドの場合は正規化
    if (field === 'shipment_date_from' || field === 'shipment_date_to') {
      value = normalizeDateValue(value);
    }
    setSearchParams((prev) => ({
      ...prev,
      [field]: value || undefined,
      page: 1, // フィルター変更時は1ページ目に戻る
    }));
  };

  /**
   * 検索の実行
   */
  const handleSearch = (searchValue: string) => {
    setSearchParams((prev) => ({
      ...prev,
      search: searchValue || undefined,
      page: 1,
    }));
  };

  /**
   * フィルターのクリア
   */
  const handleClearFilters = () => {
    setSearchParams({
      page: 1,
      page_size: 20,
      sort_by: 'created_at',
      sort_order: 'desc',
    });
  };

  /**
   * 案件を表示（詳細画面に遷移）
   */
  const handleView = (caseItem: CaseListItem) => {
    // TODO: 詳細画面の実装
    alert(`案件詳細: ${caseItem.case_number}`);
  };

  /**
   * 案件を編集
   */
  const handleEdit = async (caseItem: CaseListItem) => {
    try {
      const caseData = await getCase(caseItem.id);
      setSelectedCase(caseData);
      setModalMode('edit');
      setModalOpen(true);
    } catch (err) {
      alert('案件データの取得に失敗しました');
      console.error('Error fetching case:', err);
    }
  };

  /**
   * 新規案件作成
   */
  const handleCreate = () => {
    setSelectedCase(null);
    setModalMode('create');
    setModalOpen(true);
  };

  /**
   * モーダルを閉じる
   */
  const handleModalClose = () => {
    setModalOpen(false);
    setSelectedCase(null);
  };

  /**
   * 案件の作成・更新成功時
   */
  const handleModalSuccess = () => {
    isUserActionRef.current = true;
    fetchCases(); // 一覧を再取得
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* ヘッダー */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" fontWeight="bold">
          案件管理
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreate}
          size="large"
        >
          新規案件作成
        </Button>
      </Box>

      {/* エラー表示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* 検索・フィルター */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack spacing={2}>
          {/* 検索バー */}
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                placeholder="案件番号、顧客名、商品名で検索"
                value={searchParams.search || ''}
                onChange={(e) => handleSearch(e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
                <Button
                  variant="outlined"
                  startIcon={<FilterIcon />}
                  onClick={() => setShowFilters(!showFilters)}
                >
                  {showFilters ? 'フィルターを隠す' : 'フィルターを表示'}
                </Button>
                <Button variant="text" onClick={handleClearFilters}>
                  クリア
                </Button>
              </Box>
            </Grid>
          </Grid>

          {/* フィルター */}
          {showFilters && (
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  select
                  fullWidth
                  label="区分"
                  value={searchParams.trade_type || ''}
                  onChange={(e) => handleFilterChange('trade_type', e.target.value)}
                >
                  <MenuItem value="">すべて</MenuItem>
                  {TRADE_TYPES_ARRAY.map((type) => (
                    <MenuItem key={type} value={type}>
                      {type}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  select
                  fullWidth
                  label="ステータス"
                  value={searchParams.status || ''}
                  onChange={(e) => handleFilterChange('status', e.target.value)}
                >
                  <MenuItem value="">すべて</MenuItem>
                  {CASE_STATUSES_ARRAY.map((status) => (
                    <MenuItem key={status} value={status}>
                      {status}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  fullWidth
                  label="担当者"
                  value={searchParams.pic || ''}
                  onChange={(e) => handleFilterChange('pic', e.target.value)}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  select
                  fullWidth
                  label="ソート"
                  value={searchParams.sort_by || 'created_at'}
                  onChange={(e) => handleFilterChange('sort_by', e.target.value)}
                >
                  <MenuItem value="created_at">作成日時</MenuItem>
                  <MenuItem value="case_number">案件番号</MenuItem>
                  <MenuItem value="shipment_date">船積予定日</MenuItem>
                  <MenuItem value="sales_amount">売上額</MenuItem>
                  <MenuItem value="status">ステータス</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  type="date"
                  fullWidth
                  label="船積予定日（開始）"
                  value={normalizeDateValue(searchParams.shipment_date_from || '')}
                  onChange={(e) => handleFilterChange('shipment_date_from', e.target.value)}
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  type="date"
                  fullWidth
                  label="船積予定日（終了）"
                  value={normalizeDateValue(searchParams.shipment_date_to || '')}
                  onChange={(e) => handleFilterChange('shipment_date_to', e.target.value)}
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  select
                  fullWidth
                  label="ソート順"
                  value={searchParams.sort_order || 'desc'}
                  onChange={(e) => handleFilterChange('sort_order', e.target.value)}
                >
                  <MenuItem value="asc">昇順</MenuItem>
                  <MenuItem value="desc">降順</MenuItem>
                </TextField>
              </Grid>
            </Grid>
          )}
        </Stack>
      </Paper>

      {/* 結果表示 */}
      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="text.secondary">
          {total} 件中 {(page - 1) * pageSize + 1} 〜{' '}
          {Math.min(page * pageSize, total)} 件を表示
        </Typography>
      </Box>

      {/* テーブル */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
          <CircularProgress />
        </Box>
      ) : (
        <CaseTable
          cases={cases}
          onView={handleView}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      )}

      {/* ページネーション */}
      {totalPages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={handlePageChange}
            color="primary"
            size="large"
          />
        </Box>
      )}

      {/* 案件作成・編集モーダル */}
      <CaseFormModal
        open={modalOpen}
        onClose={handleModalClose}
        onSuccess={handleModalSuccess}
        caseData={selectedCase}
        mode={modalMode}
      />
    </Container>
  );
};
