/**
 * 変更履歴ページ
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
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
  Card,
  CardContent,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  History as HistoryIcon,
} from '@mui/icons-material';
import { getChangeHistory } from '../api/changeHistory';
import type {
  ChangeHistoryListItem,
  ChangeHistorySearchParams,
  ChangeType,
} from '../types/changeHistory';

const CHANGE_TYPES: ChangeType[] = ['CREATE', 'UPDATE', 'DELETE'];

/**
 * 変更タイプのラベル
 */
const getChangeTypeLabel = (type: ChangeType): string => {
  switch (type) {
    case 'CREATE':
      return '作成';
    case 'UPDATE':
      return '更新';
    case 'DELETE':
      return '削除';
    default:
      return type;
  }
};

/**
 * 変更タイプのアイコン
 */
const getChangeTypeIcon = (type: ChangeType): JSX.Element | undefined => {
  switch (type) {
    case 'CREATE':
      return <AddIcon fontSize="small" />;
    case 'UPDATE':
      return <EditIcon fontSize="small" />;
    case 'DELETE':
      return <DeleteIcon fontSize="small" />;
    default:
      return undefined;
  }
};

/**
 * 変更タイプの色
 */
const getChangeTypeColor = (type: ChangeType): 'success' | 'warning' | 'error' | 'default' => {
  switch (type) {
    case 'CREATE':
      return 'success';
    case 'UPDATE':
      return 'warning';
    case 'DELETE':
      return 'error';
    default:
      return 'default';
  }
};

/**
 * フィールド名のラベル
 */
const getFieldLabel = (fieldName: string): string => {
  const fieldLabels: Record<string, string> = {
    case_number: '案件番号',
    trade_type: '区分',
    customer_id: '顧客',
    supplier_name: '仕入先名',
    product_id: '商品',
    quantity: '数量',
    unit: '単位',
    sales_unit_price: '販売単価',
    purchase_unit_price: '仕入単価',
    shipment_date: '船積予定日',
    status: 'ステータス',
    pic: '担当者',
    notes: '備考',
  };
  return fieldLabels[fieldName] || fieldName;
};

/**
 * 変更履歴ページ
 */
export const ChangeHistoryPage: React.FC = () => {
  // ステート
  const [histories, setHistories] = useState<ChangeHistoryListItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedHistoryId, setExpandedHistoryId] = useState<number | null>(null);

  // フィルター
  const [searchParams, setSearchParams] = useState<ChangeHistorySearchParams>({
    page: 1,
    page_size: 20,
    sort_by: 'changed_at',
    sort_order: 'desc',
  });

  /**
   * 変更履歴一覧を取得
   */
  const fetchChangeHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getChangeHistory(searchParams);
      setHistories(response.items);
      setTotal(response.total);
      setPage(response.page);
      setTotalPages(response.total_pages);
    } catch (err) {
      setError('変更履歴の取得に失敗しました');
      console.error('Error fetching change history:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 初回レンダリング時と検索パラメータ変更時に変更履歴を取得
   */
  useEffect(() => {
    fetchChangeHistory();
  }, [searchParams]);

  /**
   * ページ変更
   */
  const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
    setSearchParams((prev) => ({ ...prev, page: value }));
  };

  /**
   * フィルターの更新
   */
  const handleFilterChange = (field: keyof ChangeHistorySearchParams, value: any) => {
    setSearchParams((prev) => ({
      ...prev,
      [field]: value || undefined,
      page: 1, // フィルター変更時は1ページ目に戻る
    }));
  };

  /**
   * アコーディオンの展開/折りたたみ
   */
  const handleAccordionChange = (historyId: number) => {
    setExpandedHistoryId(expandedHistoryId === historyId ? null : historyId);
  };

  /**
   * 日付フォーマット
   */
  const formatDateTime = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Stack spacing={3}>
        {/* タイトル */}
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            <HistoryIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
            変更履歴
          </Typography>
        </Box>

        {/* エラー表示 */}
        {error && (
          <Alert severity="error" onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {/* フィルター */}
        <Paper sx={{ p: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                label="案件番号"
                value={searchParams.case_number || ''}
                onChange={(e) =>
                  handleFilterChange('case_number', e.target.value || undefined)
                }
                placeholder="部分一致で検索"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                select
                label="変更タイプ"
                value={searchParams.change_type || ''}
                onChange={(e) => handleFilterChange('change_type', e.target.value || undefined)}
              >
                <MenuItem value="">すべて</MenuItem>
                {CHANGE_TYPES.map((type) => (
                  <MenuItem key={type} value={type}>
                    {getChangeTypeLabel(type)}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                select
                label="ソート項目"
                value={searchParams.sort_by || 'changed_at'}
                onChange={(e) => handleFilterChange('sort_by', e.target.value)}
              >
                <MenuItem value="changed_at">変更日時</MenuItem>
                <MenuItem value="id">ID</MenuItem>
                <MenuItem value="case_number">案件番号</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                select
                label="ソート順"
                value={searchParams.sort_order || 'desc'}
                onChange={(e) => handleFilterChange('sort_order', e.target.value as 'asc' | 'desc')}
              >
                <MenuItem value="desc">降順</MenuItem>
                <MenuItem value="asc">昇順</MenuItem>
              </TextField>
            </Grid>
          </Grid>
        </Paper>

        {/* ローディング */}
        {loading && (
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        )}

        {/* 変更履歴一覧 */}
        {!loading && (
          <Stack spacing={2}>
            {histories.length === 0 ? (
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <Typography color="text.secondary">変更履歴がありません</Typography>
              </Paper>
            ) : (
              histories.map((history) => (
                <Accordion
                  key={history.id}
                  expanded={expandedHistoryId === history.id}
                  onChange={() => handleAccordionChange(history.id)}
                >
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Stack direction="row" spacing={2} alignItems="center" sx={{ width: '100%' }}>
                      <Chip
                        icon={getChangeTypeIcon(history.change_type)}
                        label={getChangeTypeLabel(history.change_type)}
                        color={getChangeTypeColor(history.change_type)}
                        size="small"
                      />
                      <Typography variant="body2" sx={{ flex: 1 }}>
                        案件: {history.case_number || `ID: ${history.case_id}`}
                      </Typography>
                      {history.changed_by_name && (
                        <Typography variant="body2" color="text.secondary">
                          変更者: {history.changed_by_name}
                        </Typography>
                      )}
                      <Typography variant="body2" color="text.secondary">
                        {formatDateTime(history.changed_at)}
                      </Typography>
                    </Stack>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Card variant="outlined">
                      <CardContent>
                        <Stack spacing={2}>
                          {/* 基本情報 */}
                          <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                              <Typography variant="subtitle2" color="text.secondary">
                                案件番号
                              </Typography>
                              <Typography variant="body1">
                                {history.case_number || `ID: ${history.case_id}`}
                              </Typography>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                              <Typography variant="subtitle2" color="text.secondary">
                                変更者
                              </Typography>
                              <Typography variant="body1">
                                {history.changed_by_name || '不明'}
                              </Typography>
                            </Grid>
                            {history.field_name && (
                              <Grid item xs={12}>
                                <Typography variant="subtitle2" color="text.secondary">
                                  変更フィールド
                                </Typography>
                                <Typography variant="body1">
                                  {getFieldLabel(history.field_name)}
                                </Typography>
                              </Grid>
                            )}
                          </Grid>

                          {/* 単一フィールド変更の表示 */}
                          {history.field_name && history.old_value !== null && (
                            <Box>
                              <Typography variant="subtitle2" gutterBottom>
                                変更内容
                              </Typography>
                              <TableContainer>
                                <Table size="small">
                                  <TableBody>
                                    <TableRow>
                                      <TableCell
                                        sx={{ backgroundColor: 'error.light', color: 'error.contrastText', width: '50%' }}
                                      >
                                        変更前: {history.old_value || '(空)'}
                                      </TableCell>
                                      <TableCell
                                        sx={{ backgroundColor: 'success.light', color: 'success.contrastText', width: '50%' }}
                                      >
                                        変更後: {history.new_value || '(空)'}
                                      </TableCell>
                                    </TableRow>
                                  </TableBody>
                                </Table>
                              </TableContainer>
                            </Box>
                          )}

                          {/* 複数フィールド変更の表示 */}
                          {history.changes_json && (() => {
                            // _case_number_snapshot は表示用メタデータなので除外
                            const displayableChanges = Object.entries(history.changes_json).filter(
                              ([fieldName]) => fieldName !== '_case_number_snapshot'
                            );
                            return displayableChanges.length > 0 && (
                              <Box>
                                <Typography variant="subtitle2" gutterBottom>
                                  変更内容
                                </Typography>
                                <TableContainer>
                                  <Table size="small">
                                    <TableHead>
                                      <TableRow>
                                        <TableCell>フィールド</TableCell>
                                        <TableCell sx={{ backgroundColor: 'error.light', color: 'error.contrastText' }}>
                                          変更前
                                        </TableCell>
                                        <TableCell sx={{ backgroundColor: 'success.light', color: 'success.contrastText' }}>
                                          変更後
                                        </TableCell>
                                      </TableRow>
                                    </TableHead>
                                    <TableBody>
                                      {displayableChanges.map(([fieldName, change]) => {
                                        // changeがオブジェクト（{old, new}形式）か文字列かを判定
                                        const isChangeObject = change && typeof change === 'object' && ('old' in change || 'new' in change);
                                        const oldValue = isChangeObject ? (change as { old?: string | null; new?: string | null }).old : null;
                                        const newValue = isChangeObject ? (change as { old?: string | null; new?: string | null }).new : null;

                                        return (
                                          <TableRow key={fieldName}>
                                            <TableCell>{getFieldLabel(fieldName)}</TableCell>
                                            <TableCell sx={{ backgroundColor: 'error.light', color: 'error.contrastText' }}>
                                              {oldValue || '(空)'}
                                            </TableCell>
                                            <TableCell sx={{ backgroundColor: 'success.light', color: 'success.contrastText' }}>
                                              {newValue || '(空)'}
                                            </TableCell>
                                          </TableRow>
                                        );
                                      })}
                                    </TableBody>
                                  </Table>
                                </TableContainer>
                              </Box>
                            );
                          })()}

                          {/* 備考 */}
                          {history.notes && (
                            <Box>
                              <Typography variant="subtitle2" color="text.secondary">
                                備考
                              </Typography>
                              <Typography variant="body2">{history.notes}</Typography>
                            </Box>
                          )}
                        </Stack>
                      </CardContent>
                    </Card>
                  </AccordionDetails>
                </Accordion>
              ))
            )}

            {/* ページネーション */}
            {totalPages > 1 && (
              <Box display="flex" justifyContent="center" mt={3}>
                <Pagination
                  count={totalPages}
                  page={page}
                  onChange={handlePageChange}
                  color="primary"
                  size="large"
                />
              </Box>
            )}

            {/* 件数表示 */}
            <Typography variant="body2" color="text.secondary" textAlign="center">
              全 {total} 件
            </Typography>
          </Stack>
        )}
      </Stack>
    </Container>
  );
};
