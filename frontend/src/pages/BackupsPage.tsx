/**
 * バックアップ管理ページ
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
  Tooltip,
  TextField,
  MenuItem,
  Grid,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Pagination,
  Stack,
} from '@mui/material';
import {
  Backup as BackupIcon,
  Restore as RestoreIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  Refresh as RefreshIcon,
  DeleteSweep as CleanupIcon,
} from '@mui/icons-material';
import {
  getBackups,
  createBackup,
  restoreBackup,
  deleteBackup,
  cleanupBackups,
} from '../api/backups';
import type { Backup, BackupSearchParams, BackupType, BackupStatus } from '../types/backup';

const BACKUP_TYPES: BackupType[] = ['manual', 'auto', 'scheduled'];
const BACKUP_STATUSES: BackupStatus[] = ['success', 'failed', 'in_progress'];

/**
 * バックアップタイプのラベル
 */
const getBackupTypeLabel = (type: BackupType): string => {
  switch (type) {
    case 'manual':
      return '手動';
    case 'auto':
      return '自動';
    case 'scheduled':
      return 'スケジュール';
    default:
      return type;
  }
};

/**
 * ステータスの色を取得
 */
const getStatusColor = (status: BackupStatus): 'success' | 'error' | 'warning' | 'default' => {
  switch (status) {
    case 'success':
      return 'success';
    case 'failed':
      return 'error';
    case 'in_progress':
      return 'warning';
    default:
      return 'default';
  }
};

/**
 * ステータスのラベル
 */
const getStatusLabel = (status: BackupStatus): string => {
  switch (status) {
    case 'success':
      return '成功';
    case 'failed':
      return '失敗';
    case 'in_progress':
      return '実行中';
    default:
      return status;
  }
};

/**
 * ファイルサイズをフォーマット
 */
const formatFileSize = (bytes: number | null): string => {
  if (!bytes) return '-';
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
};

/**
 * 日付をフォーマット
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

/**
 * バックアップ管理ページ
 */
export const BackupsPage: React.FC = () => {
  const [backups, setBackups] = useState<Backup[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // ダイアログ
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [restoreDialogOpen, setRestoreDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedBackup, setSelectedBackup] = useState<Backup | null>(null);
  const [newBackupName, setNewBackupName] = useState('');
  const [creating, setCreating] = useState(false);

  // フィルター
  const [searchParams, setSearchParams] = useState<BackupSearchParams>({
    page: 1,
    page_size: 20,
    sort_by: 'created_at',
    sort_order: 'desc',
  });

  /**
   * バックアップ一覧を取得
   */
  const fetchBackups = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const response = await getBackups(searchParams);
      setBackups(response.items);
      setTotal(response.total);
      setPage(response.page);
      setTotalPages(response.total_pages);
    } catch (err: any) {
      setError('バックアップ一覧の取得に失敗しました');
      console.error('Error fetching backups:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 初回レンダリング時と検索パラメータ変更時にバックアップを取得
   */
  useEffect(() => {
    fetchBackups();
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
  const handleFilterChange = (field: keyof BackupSearchParams, value: any) => {
    setSearchParams((prev) => ({
      ...prev,
      [field]: value || undefined,
      page: 1, // フィルター変更時は1ページ目に戻る
    }));
  };

  /**
   * バックアップを作成
   */
  const handleCreateBackup = async () => {
    if (creating) return;

    setCreating(true);
    setError(null);
    setSuccess(null);
    try {
      await createBackup({
        backup_name: newBackupName || undefined,
        backup_type: 'manual',
      });
      setSuccess('バックアップが作成されました');
      setCreateDialogOpen(false);
      setNewBackupName('');
      fetchBackups();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'バックアップの作成に失敗しました');
    } finally {
      setCreating(false);
    }
  };

  /**
   * バックアップから復元
   */
  const handleRestoreBackup = async () => {
    if (!selectedBackup) return;

    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      await restoreBackup(selectedBackup.id);
      setSuccess('バックアップから復元が完了しました');
      setRestoreDialogOpen(false);
      setSelectedBackup(null);
      fetchBackups();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'バックアップの復元に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  /**
   * バックアップを削除
   */
  const handleDeleteBackup = async () => {
    if (!selectedBackup) return;

    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      await deleteBackup(selectedBackup.id);
      setSuccess('バックアップが削除されました');
      setDeleteDialogOpen(false);
      setSelectedBackup(null);
      fetchBackups();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'バックアップの削除に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  /**
   * 古いバックアップをクリーンアップ
   */
  const handleCleanupBackups = async () => {
    if (!confirm('30日以上前のバックアップを削除しますか？')) return;

    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const result = await cleanupBackups(30);
      setSuccess(result.message);
      fetchBackups();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'バックアップのクリーンアップに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Stack spacing={3}>
        {/* タイトル */}
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            <BackupIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
            バックアップ管理
          </Typography>
        </Box>

        {/* メッセージ表示 */}
        {error && (
          <Alert severity="error" onClose={() => setError(null)}>
            {error}
          </Alert>
        )}
        {success && (
          <Alert severity="success" onClose={() => setSuccess(null)}>
            {success}
          </Alert>
        )}

        {/* アクションボタン */}
        <Paper sx={{ p: 2 }}>
          <Stack direction="row" spacing={2}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setCreateDialogOpen(true)}
            >
              バックアップ作成
            </Button>
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={fetchBackups}
              disabled={loading}
            >
              更新
            </Button>
            <Button
              variant="outlined"
              color="warning"
              startIcon={<CleanupIcon />}
              onClick={handleCleanupBackups}
              disabled={loading}
            >
              古いバックアップを削除
            </Button>
          </Stack>
        </Paper>

        {/* フィルター */}
        <Paper sx={{ p: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                select
                label="バックアップタイプ"
                value={searchParams.backup_type || ''}
                onChange={(e) => handleFilterChange('backup_type', e.target.value || undefined)}
              >
                <MenuItem value="">すべて</MenuItem>
                {BACKUP_TYPES.map((type) => (
                  <MenuItem key={type} value={type}>
                    {getBackupTypeLabel(type)}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                select
                label="ステータス"
                value={searchParams.status || ''}
                onChange={(e) => handleFilterChange('status', e.target.value || undefined)}
              >
                <MenuItem value="">すべて</MenuItem>
                {BACKUP_STATUSES.map((status) => (
                  <MenuItem key={status} value={status}>
                    {getStatusLabel(status)}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                select
                label="ソート項目"
                value={searchParams.sort_by || 'created_at'}
                onChange={(e) => handleFilterChange('sort_by', e.target.value)}
              >
                <MenuItem value="created_at">作成日時</MenuItem>
                <MenuItem value="id">ID</MenuItem>
                <MenuItem value="backup_name">バックアップ名</MenuItem>
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

        {/* バックアップ一覧 */}
        {!loading && (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>バックアップ名</TableCell>
                  <TableCell>タイプ</TableCell>
                  <TableCell>ステータス</TableCell>
                  <TableCell>ファイルサイズ</TableCell>
                  <TableCell>レコード数</TableCell>
                  <TableCell>作成日時</TableCell>
                  <TableCell align="right">操作</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {backups.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={8} align="center">
                      <Typography color="text.secondary" sx={{ py: 4 }}>
                        バックアップがありません
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  backups.map((backup) => (
                    <TableRow key={backup.id}>
                      <TableCell>{backup.id}</TableCell>
                      <TableCell>{backup.backup_name}</TableCell>
                      <TableCell>
                        <Chip
                          label={getBackupTypeLabel(backup.backup_type)}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={getStatusLabel(backup.status)}
                          color={getStatusColor(backup.status)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{formatFileSize(backup.file_size)}</TableCell>
                      <TableCell>{backup.record_count || '-'}</TableCell>
                      <TableCell>{formatDateTime(backup.created_at)}</TableCell>
                      <TableCell align="right">
                        <Stack direction="row" spacing={1} justifyContent="flex-end">
                          {backup.status === 'success' && (
                            <>
                              <Tooltip title="復元">
                                <IconButton
                                  size="small"
                                  color="primary"
                                  onClick={() => {
                                    setSelectedBackup(backup);
                                    setRestoreDialogOpen(true);
                                  }}
                                >
                                  <RestoreIcon />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="削除">
                                <IconButton
                                  size="small"
                                  color="error"
                                  onClick={() => {
                                    setSelectedBackup(backup);
                                    setDeleteDialogOpen(true);
                                  }}
                                >
                                  <DeleteIcon />
                                </IconButton>
                              </Tooltip>
                            </>
                          )}
                          {backup.error_message && (
                            <Tooltip title={backup.error_message}>
                              <Alert severity="error" sx={{ p: 0.5 }}>
                                !
                              </Alert>
                            </Tooltip>
                          )}
                        </Stack>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        {/* ページネーション */}
        {totalPages > 1 && (
          <Box display="flex" justifyContent="center">
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

      {/* バックアップ作成ダイアログ */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)}>
        <DialogTitle>バックアップ作成</DialogTitle>
        <DialogContent>
          <DialogContentText>バックアップを作成します。バックアップ名を入力してください（空欄の場合は自動生成されます）。</DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            label="バックアップ名"
            fullWidth
            variant="standard"
            value={newBackupName}
            onChange={(e) => setNewBackupName(e.target.value)}
            disabled={creating}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)} disabled={creating}>
            キャンセル
          </Button>
          <Button onClick={handleCreateBackup} variant="contained" disabled={creating}>
            {creating ? <CircularProgress size={20} /> : '作成'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* 復元確認ダイアログ */}
      <Dialog open={restoreDialogOpen} onClose={() => setRestoreDialogOpen(false)}>
        <DialogTitle>バックアップから復元</DialogTitle>
        <DialogContent>
          <DialogContentText>
            バックアップ「{selectedBackup?.backup_name}」からデータを復元しますか？
            <br />
            現在のデータベースは上書きされます。この操作は元に戻せません。
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRestoreDialogOpen(false)} disabled={loading}>
            キャンセル
          </Button>
          <Button onClick={handleRestoreBackup} variant="contained" color="warning" disabled={loading}>
            {loading ? <CircularProgress size={20} /> : '復元'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* 削除確認ダイアログ */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>バックアップ削除</DialogTitle>
        <DialogContent>
          <DialogContentText>
            バックアップ「{selectedBackup?.backup_name}」を削除しますか？
            <br />
            この操作は元に戻せません。
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)} disabled={loading}>
            キャンセル
          </Button>
          <Button onClick={handleDeleteBackup} variant="contained" color="error" disabled={loading}>
            {loading ? <CircularProgress size={20} /> : '削除'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};
