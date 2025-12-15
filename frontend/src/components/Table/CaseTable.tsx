/**
 * 案件一覧テーブル
 */
import React, { useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  Box,
  Typography,
  Tooltip,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Description as DocumentIcon,
  Receipt as InvoiceIcon,
  LocalShipping as PackingListIcon,
} from '@mui/icons-material';
import type { CaseListItem } from '../../types/case';
import { generateInvoice, generatePackingList, downloadDocument } from '../../api/documents';

interface CaseTableProps {
  cases: CaseListItem[];
  onView?: (caseItem: CaseListItem) => void;
  onEdit?: (caseItem: CaseListItem) => void;
  onDelete?: (caseItem: CaseListItem) => void;
  onDocumentGenerated?: () => void;
}

/**
 * ステータスの色を取得
 */
const getStatusColor = (status: string) => {
  switch (status) {
    case '見積中':
      return 'default';
    case '受注済':
      return 'primary';
    case '船積済':
      return 'info';
    case '完了':
      return 'success';
    case 'キャンセル':
      return 'error';
    default:
      return 'default';
  }
};

/**
 * 金額をフォーマット
 */
const formatAmount = (amount?: number | string | null): string => {
  if (amount === undefined || amount === null) return '-';
  const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (isNaN(numAmount)) return '-';
  return new Intl.NumberFormat('ja-JP', {
    style: 'currency',
    currency: 'JPY',
  }).format(numAmount);
};

/**
 * パーセンテージをフォーマット
 */
const formatPercentage = (rate?: number | string | null): string => {
  if (rate === undefined || rate === null) return '-';
  const numRate = typeof rate === 'string' ? parseFloat(rate) : rate;
  if (isNaN(numRate)) return '-';
  return `${numRate.toFixed(2)}%`;
};

/**
 * 日付をフォーマット
 */
const formatDate = (dateString?: string | null): string => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('ja-JP');
};

/**
 * 案件一覧テーブルコンポーネント
 */
export const CaseTable: React.FC<CaseTableProps> = ({
  cases,
  onView,
  onEdit,
  onDelete,
  onDocumentGenerated,
}) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedCaseId, setSelectedCaseId] = useState<number | null>(null);
  const [generatingDoc, setGeneratingDoc] = useState<number | null>(null);

  // ドキュメントメニューを開く
  const handleOpenDocMenu = (event: React.MouseEvent<HTMLElement>, caseId: number) => {
    setAnchorEl(event.currentTarget);
    setSelectedCaseId(caseId);
  };

  // ドキュメントメニューを閉じる
  const handleCloseDocMenu = () => {
    setAnchorEl(null);
    setSelectedCaseId(null);
  };

  // Invoice生成
  const handleGenerateInvoice = async () => {
    if (!selectedCaseId) return;
    
    setGeneratingDoc(selectedCaseId);
    handleCloseDocMenu();
    
    try {
      const document = await generateInvoice(selectedCaseId);
      // 生成後すぐにダウンロード
      await downloadDocument(document.id);
      alert('Invoice を生成しました');
      if (onDocumentGenerated) {
        onDocumentGenerated();
      }
    } catch (error) {
      console.error('Invoice generation failed:', error);
      alert('Invoice の生成に失敗しました');
    } finally {
      setGeneratingDoc(null);
    }
  };

  // Packing List生成
  const handleGeneratePackingList = async () => {
    if (!selectedCaseId) return;
    
    setGeneratingDoc(selectedCaseId);
    handleCloseDocMenu();
    
    try {
      const document = await generatePackingList(selectedCaseId);
      // 生成後すぐにダウンロード
      await downloadDocument(document.id);
      alert('Packing List を生成しました');
      if (onDocumentGenerated) {
        onDocumentGenerated();
      }
    } catch (error) {
      console.error('Packing List generation failed:', error);
      alert('Packing List の生成に失敗しました');
    } finally {
      setGeneratingDoc(null);
    }
  };

  if (cases.length === 0) {
    return (
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="body1" color="text.secondary">
          案件が見つかりません
        </Typography>
      </Paper>
    );
  }

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>案件番号</TableCell>
            <TableCell>区分</TableCell>
            <TableCell>顧客名</TableCell>
            <TableCell>商品名</TableCell>
            <TableCell align="right">数量</TableCell>
            <TableCell align="right">売上額</TableCell>
            <TableCell align="right">粗利額</TableCell>
            <TableCell align="right">粗利率</TableCell>
            <TableCell>ステータス</TableCell>
            <TableCell>担当者</TableCell>
            <TableCell>船積予定日</TableCell>
            <TableCell align="center">操作</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {cases.map((caseItem) => (
            <TableRow key={caseItem.id} hover>
              <TableCell>
                <Typography variant="body2" fontWeight="medium">
                  {caseItem.case_number}
                </Typography>
              </TableCell>
              <TableCell>
                <Chip
                  label={caseItem.trade_type}
                  size="small"
                  color={caseItem.trade_type === '輸出' ? 'primary' : 'secondary'}
                />
              </TableCell>
              <TableCell>{caseItem.customer_name || '-'}</TableCell>
              <TableCell>{caseItem.product_name || '-'}</TableCell>
              <TableCell align="right">
                {Number(caseItem.quantity).toLocaleString()} {caseItem.unit}
              </TableCell>
              <TableCell align="right">{formatAmount(caseItem.sales_amount)}</TableCell>
              <TableCell align="right">{formatAmount(caseItem.gross_profit)}</TableCell>
              <TableCell align="right">{formatPercentage(caseItem.gross_profit_rate)}</TableCell>
              <TableCell>
                <Chip
                  label={caseItem.status}
                  size="small"
                  color={getStatusColor(caseItem.status)}
                />
              </TableCell>
              <TableCell>{caseItem.pic}</TableCell>
              <TableCell>{formatDate(caseItem.shipment_date)}</TableCell>
              <TableCell align="center">
                <Box sx={{ display: 'flex', justifyContent: 'center', gap: 0.5 }}>
                  {onView && (
                    <Tooltip title="詳細表示">
                      <IconButton size="small" onClick={() => onView(caseItem)}>
                        <ViewIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  )}
                  {onEdit && (
                    <Tooltip title="編集">
                      <IconButton size="small" onClick={() => onEdit(caseItem)}>
                        <EditIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  )}
                  <Tooltip title="ドキュメント生成">
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={(e) => handleOpenDocMenu(e, caseItem.id)}
                      disabled={generatingDoc === caseItem.id}
                    >
                      {generatingDoc === caseItem.id ? (
                        <CircularProgress size={16} />
                      ) : (
                        <DocumentIcon fontSize="small" />
                      )}
                    </IconButton>
                  </Tooltip>
                  {onDelete && (
                    <Tooltip title="削除">
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => onDelete(caseItem)}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  )}
                </Box>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* ドキュメント生成メニュー */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleCloseDocMenu}
      >
        <MenuItem onClick={handleGenerateInvoice}>
          <ListItemIcon>
            <InvoiceIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Invoice 生成</ListItemText>
        </MenuItem>
        <MenuItem onClick={handleGeneratePackingList}>
          <ListItemIcon>
            <PackingListIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Packing List 生成</ListItemText>
        </MenuItem>
      </Menu>
    </TableContainer>
  );
};

