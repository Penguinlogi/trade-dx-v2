/**
 * ドキュメント履歴ページ
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
} from '@mui/material';
import {
  Download as DownloadIcon,
  Receipt as InvoiceIcon,
  LocalShipping as PackingListIcon,
} from '@mui/icons-material';
import { getDocuments, downloadDocument, type Document, type DocumentType } from '../api/documents';

/**
 * ドキュメントタイプのラベル
 */
const getDocumentTypeLabel = (type: DocumentType): string => {
  switch (type) {
    case 'invoice':
      return 'Invoice';
    case 'packing_list':
      return 'Packing List';
    default:
      return type;
  }
};

/**
 * ドキュメントタイプのアイコン
 */
const getDocumentTypeIcon = (type: DocumentType): JSX.Element | undefined => {
  switch (type) {
    case 'invoice':
      return <InvoiceIcon fontSize="small" />;
    case 'packing_list':
      return <PackingListIcon fontSize="small" />;
    default:
      return undefined;
  }
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
 * ドキュメント履歴ページ
 */
export const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState<number | null>(null);

  // フィルター
  const [filterType, setFilterType] = useState<DocumentType | ''>('');
  const [filterCaseId, setFilterCaseId] = useState<string>('');

  /**
   * ドキュメント一覧を取得
   */
  const fetchDocuments = async () => {
    setLoading(true);
    setError(null);
    try {
      const params: any = {
        limit: 100,
      };

      if (filterType) {
        params.document_type = filterType;
      }

      if (filterCaseId) {
        const caseId = parseInt(filterCaseId, 10);
        if (!isNaN(caseId)) {
          params.case_id = caseId;
        }
      }

      const response = await getDocuments(params);
      setDocuments(response.documents);
      setTotal(response.total);
    } catch (err) {
      setError('ドキュメント履歴の取得に失敗しました');
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 初回レンダリング時とフィルター変更時にドキュメントを取得
   */
  useEffect(() => {
    fetchDocuments();
  }, [filterType, filterCaseId]);

  /**
   * ドキュメントダウンロード
   */
  const handleDownload = async (documentId: number) => {
    setDownloading(documentId);
    try {
      await downloadDocument(documentId);
    } catch (err) {
      console.error('Download failed:', err);
      alert('ダウンロードに失敗しました');
    } finally {
      setDownloading(null);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight="bold" gutterBottom>
          ドキュメント履歴
        </Typography>
        <Typography variant="body2" color="text.secondary">
          生成されたドキュメント（Invoice、Packing List）の履歴を確認できます
        </Typography>
      </Box>

      {/* フィルター */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              select
              fullWidth
              label="ドキュメントタイプ"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value as DocumentType | '')}
            >
              <MenuItem value="">すべて</MenuItem>
              <MenuItem value="invoice">Invoice</MenuItem>
              <MenuItem value="packing_list">Packing List</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="案件ID"
              value={filterCaseId}
              onChange={(e) => setFilterCaseId(e.target.value)}
              placeholder="例: 123"
              type="number"
            />
          </Grid>
        </Grid>
      </Paper>

      {/* エラー表示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* ローディング表示 */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
          <CircularProgress />
        </Box>
      ) : documents.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="body1" color="text.secondary">
            ドキュメントが見つかりません
          </Typography>
        </Paper>
      ) : (
        <>
          {/* 件数表示 */}
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary">
              全 {total} 件のドキュメント
            </Typography>
          </Box>

          {/* テーブル */}
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>タイプ</TableCell>
                  <TableCell>案件ID</TableCell>
                  <TableCell>ファイル名</TableCell>
                  <TableCell>テンプレート</TableCell>
                  <TableCell>生成日時</TableCell>
                  <TableCell>備考</TableCell>
                  <TableCell align="center">操作</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {documents.map((doc) => (
                  <TableRow key={doc.id} hover>
                    <TableCell>{doc.id}</TableCell>
                    <TableCell>
                      <Chip
                        icon={getDocumentTypeIcon(doc.document_type)}
                        label={getDocumentTypeLabel(doc.document_type)}
                        size="small"
                        color={doc.document_type === 'invoice' ? 'primary' : 'secondary'}
                      />
                    </TableCell>
                    <TableCell>{doc.case_id}</TableCell>
                    <TableCell>
                      <Typography variant="body2" noWrap sx={{ maxWidth: 250 }}>
                        {doc.file_name}
                      </Typography>
                    </TableCell>
                    <TableCell>{doc.template_name || '-'}</TableCell>
                    <TableCell>{formatDateTime(doc.generated_at)}</TableCell>
                    <TableCell>
                      <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                        {doc.notes || '-'}
                      </Typography>
                    </TableCell>
                    <TableCell align="center">
                      <Tooltip title="ダウンロード">
                        <IconButton
                          size="small"
                          color="primary"
                          onClick={() => handleDownload(doc.id)}
                          disabled={downloading === doc.id}
                        >
                          {downloading === doc.id ? (
                            <CircularProgress size={20} />
                          ) : (
                            <DownloadIcon />
                          )}
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}
    </Container>
  );
};
