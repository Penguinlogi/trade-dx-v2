/**
 * 案件作成・編集モーダル
 */
import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Grid,
  MenuItem,
  Box,
  CircularProgress,
  Alert,
  IconButton,
  Tooltip,
} from '@mui/material';
import { AutoAwesome as AutoIcon } from '@mui/icons-material';
import { createCase, updateCase } from '../../api/cases';
import { generateCaseNumber } from '../../api/caseNumbers';
import type {
  Case,
  CaseCreateRequest,
  CaseUpdateRequest,
  TradeType,
  CaseStatus,
} from '../../types/case';

const TRADE_TYPES: TradeType[] = ['輸出', '輸入'];
const CASE_STATUSES: CaseStatus[] = ['見積中', '受注済', '船積済', '完了', 'キャンセル'];

interface CaseFormModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
  caseData?: Case | null;
  mode: 'create' | 'edit';
}

interface FormData {
  case_number: string;
  trade_type: string;
  customer_id: string;
  supplier_name: string;
  product_id: string;
  quantity: string;
  unit: string;
  sales_unit_price: string;
  purchase_unit_price: string;
  shipment_date: string;
  status: string;
  pic: string;
  notes: string;
}

const initialFormData: FormData = {
  case_number: '',
  trade_type: '輸出',
  customer_id: '',
  supplier_name: '',
  product_id: '',
  quantity: '',
  unit: '',
  sales_unit_price: '',
  purchase_unit_price: '',
  shipment_date: '',
  status: '見積中',
  pic: '',
  notes: '',
};

/**
 * 案件フォームモーダル
 */
export const CaseFormModal: React.FC<CaseFormModalProps> = ({
  open,
  onClose,
  onSuccess,
  caseData,
  mode,
}) => {
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState<Partial<Record<keyof FormData, string>>>({});
  const [generatingNumber, setGeneratingNumber] = useState(false);

  /**
   * 編集モードの場合、案件データをフォームにセット
   */
  useEffect(() => {
    if (mode === 'edit' && caseData) {
      setFormData({
        case_number: caseData.case_number || '',
        trade_type: caseData.trade_type || '輸出',
        customer_id: caseData.customer_id?.toString() || '',
        supplier_name: caseData.supplier_name || '',
        product_id: caseData.product_id?.toString() || '',
        quantity: caseData.quantity?.toString() || '',
        unit: caseData.unit || '',
        sales_unit_price: caseData.sales_unit_price?.toString() || '',
        purchase_unit_price: caseData.purchase_unit_price?.toString() || '',
        shipment_date: caseData.shipment_date || '',
        status: caseData.status || '見積中',
        pic: caseData.pic || '',
        notes: caseData.notes || '',
      });
    } else {
      setFormData(initialFormData);
    }
    setError(null);
    setErrors({});
  }, [mode, caseData, open]);

  /**
   * 日付の値を検証（年の部分が4桁を超えないようにする）
   */
  const validateDateValue = (dateValue: string): string => {
    if (!dateValue) return dateValue;

    // YYYY-MM-DD形式を検証
    const dateRegex = /^(\d{4})-(\d{2})-(\d{2})$/;
    const match = dateValue.match(dateRegex);

    if (match) {
      const [, year, month, day] = match;
      const validYear = (year || '').substring(0, 4);
      return `${validYear}-${month}-${day}`;
    }

    return dateValue;
  };

  /**
   * フォーム入力変更
   */
  const handleChange = (field: keyof FormData, value: string) => {
    // 日付フィールドの場合は値を検証
    if (field === 'shipment_date') {
      value = validateDateValue(value);
    }

    setFormData((prev) => ({ ...prev, [field]: value }));
    // エラーをクリア
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  /**
   * 案件番号を自動生成
   */
  const handleGenerateCaseNumber = async () => {
    if (!formData.trade_type) {
      alert('区分を選択してください');
      return;
    }

    setGeneratingNumber(true);
    try {
      const result = await generateCaseNumber(formData.trade_type);
      setFormData((prev) => ({ ...prev, case_number: result.case_number }));
    } catch (err) {
      console.error('Error generating case number:', err);
      alert('案件番号の生成に失敗しました');
    } finally {
      setGeneratingNumber(false);
    }
  };

  /**
   * バリデーション
   */
  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof FormData, string>> = {};

    if (!formData.trade_type) {
      newErrors.trade_type = '区分は必須です';
    }
    if (!formData.customer_id) {
      newErrors.customer_id = '顧客IDは必須です';
    }
    if (!formData.product_id) {
      newErrors.product_id = '商品IDは必須です';
    }
    if (!formData.quantity || parseFloat(formData.quantity) <= 0) {
      newErrors.quantity = '数量は1以上である必要があります';
    }
    if (!formData.unit) {
      newErrors.unit = '単位は必須です';
    }
    if (!formData.sales_unit_price || parseFloat(formData.sales_unit_price) < 0) {
      newErrors.sales_unit_price = '販売単価は0以上である必要があります';
    }
    if (!formData.purchase_unit_price || parseFloat(formData.purchase_unit_price) < 0) {
      newErrors.purchase_unit_price = '仕入単価は0以上である必要があります';
    }
    if (!formData.status) {
      newErrors.status = 'ステータスは必須です';
    }
    if (!formData.pic) {
      newErrors.pic = '担当者は必須です';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * フォーム送信
   */
  const handleSubmit = async () => {
    if (!validate()) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      if (mode === 'create') {
        // 新規作成
        const data: CaseCreateRequest = {
          case_number: formData.case_number || undefined,
          trade_type: formData.trade_type,
          customer_id: parseInt(formData.customer_id),
          supplier_name: formData.supplier_name || undefined,
          product_id: parseInt(formData.product_id),
          quantity: parseFloat(formData.quantity),
          unit: formData.unit,
          sales_unit_price: parseFloat(formData.sales_unit_price),
          purchase_unit_price: parseFloat(formData.purchase_unit_price),
          shipment_date: formData.shipment_date || undefined,
          status: formData.status,
          pic: formData.pic,
          notes: formData.notes || undefined,
        };
        await createCase(data);
      } else if (mode === 'edit' && caseData) {
        // 更新
        const data: CaseUpdateRequest = {
          trade_type: formData.trade_type,
          customer_id: parseInt(formData.customer_id),
          supplier_name: formData.supplier_name || undefined,
          product_id: parseInt(formData.product_id),
          quantity: parseFloat(formData.quantity),
          unit: formData.unit,
          sales_unit_price: parseFloat(formData.sales_unit_price),
          purchase_unit_price: parseFloat(formData.purchase_unit_price),
          shipment_date: formData.shipment_date || undefined,
          status: formData.status,
          pic: formData.pic,
          notes: formData.notes || undefined,
        };
        await updateCase(caseData.id, data);
      }

      onSuccess();
      onClose();
    } catch (err: any) {
      console.error('Error saving case:', err);
      setError(err.response?.data?.detail || '案件の保存に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {mode === 'create' ? '新規案件作成' : '案件編集'}
      </DialogTitle>
      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box sx={{ mt: 2 }}>
          <Grid container spacing={2}>
            {/* 案件番号（任意） */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="案件番号（任意）"
                value={formData.case_number}
                onChange={(e) => handleChange('case_number', e.target.value)}
                error={!!errors.case_number}
                helperText={errors.case_number || '空白の場合は自動生成されます'}
                disabled={mode === 'edit' || generatingNumber}
                InputProps={{
                  endAdornment: mode === 'create' && (
                    <Tooltip title="案件番号を自動生成">
                      <IconButton
                        onClick={handleGenerateCaseNumber}
                        disabled={generatingNumber || !formData.trade_type}
                        size="small"
                      >
                        {generatingNumber ? <CircularProgress size={20} /> : <AutoIcon />}
                      </IconButton>
                    </Tooltip>
                  ),
                }}
              />
            </Grid>

            {/* 区分 */}
            <Grid item xs={12} sm={6}>
              <TextField
                select
                fullWidth
                required
                label="区分"
                value={formData.trade_type}
                onChange={(e) => handleChange('trade_type', e.target.value)}
                error={!!errors.trade_type}
                helperText={errors.trade_type}
              >
                {TRADE_TYPES.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {/* 顧客ID */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                label="顧客ID"
                type="number"
                value={formData.customer_id}
                onChange={(e) => handleChange('customer_id', e.target.value)}
                error={!!errors.customer_id}
                helperText={errors.customer_id}
              />
            </Grid>

            {/* 仕入先名 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="仕入先名"
                value={formData.supplier_name}
                onChange={(e) => handleChange('supplier_name', e.target.value)}
              />
            </Grid>

            {/* 商品ID */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                label="商品ID"
                type="number"
                value={formData.product_id}
                onChange={(e) => handleChange('product_id', e.target.value)}
                error={!!errors.product_id}
                helperText={errors.product_id}
              />
            </Grid>

            {/* 数量 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                label="数量"
                type="number"
                value={formData.quantity}
                onChange={(e) => handleChange('quantity', e.target.value)}
                error={!!errors.quantity}
                helperText={errors.quantity}
              />
            </Grid>

            {/* 単位 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                label="単位"
                value={formData.unit}
                onChange={(e) => handleChange('unit', e.target.value)}
                error={!!errors.unit}
                helperText={errors.unit}
              />
            </Grid>

            {/* 販売単価 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                label="販売単価"
                type="number"
                value={formData.sales_unit_price}
                onChange={(e) => handleChange('sales_unit_price', e.target.value)}
                error={!!errors.sales_unit_price}
                helperText={errors.sales_unit_price}
              />
            </Grid>

            {/* 仕入単価 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                label="仕入単価"
                type="number"
                value={formData.purchase_unit_price}
                onChange={(e) => handleChange('purchase_unit_price', e.target.value)}
                error={!!errors.purchase_unit_price}
                helperText={errors.purchase_unit_price}
              />
            </Grid>

            {/* 船積予定日 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="船積予定日"
                type="date"
                value={formData.shipment_date}
                onChange={(e) => handleChange('shipment_date', e.target.value)}
                InputLabelProps={{ shrink: true }}
                inputProps={{
                  max: '2099-12-31',
                  min: '1900-01-01',
                }}
              />
            </Grid>

            {/* ステータス */}
            <Grid item xs={12} sm={6}>
              <TextField
                select
                fullWidth
                required
                label="ステータス"
                value={formData.status}
                onChange={(e) => handleChange('status', e.target.value)}
                error={!!errors.status}
                helperText={errors.status}
              >
                {CASE_STATUSES.map((status) => (
                  <MenuItem key={status} value={status}>
                    {status}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {/* 担当者 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                label="担当者"
                value={formData.pic}
                onChange={(e) => handleChange('pic', e.target.value)}
                error={!!errors.pic}
                helperText={errors.pic}
              />
            </Grid>

            {/* 備考 */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="備考"
                multiline
                rows={3}
                value={formData.notes}
                onChange={(e) => handleChange('notes', e.target.value)}
              />
            </Grid>
          </Grid>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          キャンセル
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading}
          startIcon={loading ? <CircularProgress size={20} /> : null}
        >
          {mode === 'create' ? '作成' : '更新'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
