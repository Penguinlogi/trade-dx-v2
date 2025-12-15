/**
 * 商品マスタ一覧ページ
 */
import React, { useState, useEffect } from 'react';
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
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Inventory as InventoryIcon,
} from '@mui/icons-material';
import { getProducts, deleteProduct, getCategories } from '../api/products';
import type { Product, ProductFilters } from '../types/product';

/**
 * 商品マスタ一覧ページ
 */
export const ProductsPage: React.FC = () => {
  // ステート
  const [products, setProducts] = useState<Product[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [categories, setCategories] = useState<string[]>([]);

  // フィルター
  const [filters, setFilters] = useState<ProductFilters>({
    page: 1,
    page_size: 20,
    is_active: 1,
  });
  const [searchInput, setSearchInput] = useState('');

  /**
   * 商品一覧を取得
   */
  const fetchProducts = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getProducts(filters);
      setProducts(response.items);
      setTotal(response.total);
      setPage(response.page);
      setTotalPages(response.total_pages);
    } catch (err) {
      setError('商品一覧の取得に失敗しました');
      console.error('Error fetching products:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * カテゴリ一覧を取得
   */
  const fetchCategories = async () => {
    try {
      const cats = await getCategories();
      setCategories(cats);
    } catch (err) {
      console.error('Error fetching categories:', err);
    }
  };

  /**
   * 初回レンダリング時にカテゴリを取得
   */
  useEffect(() => {
    fetchCategories();
  }, []);

  /**
   * フィルター変更時に商品を取得
   */
  useEffect(() => {
    fetchProducts();
  }, [filters]);

  /**
   * ページ変更
   */
  const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
    setFilters((prev) => ({ ...prev, page: value }));
  };

  /**
   * 検索実行
   */
  const handleSearch = () => {
    setFilters((prev) => ({
      ...prev,
      search: searchInput || undefined,
      page: 1,
    }));
  };

  /**
   * カテゴリフィルタ変更
   */
  const handleCategoryChange = (value: string) => {
    const category = value === 'all' ? undefined : value;
    setFilters((prev) => ({ ...prev, category, page: 1 }));
  };

  /**
   * 有効フラグフィルタ変更
   */
  const handleActiveFilterChange = (value: string) => {
    const isActive = value === 'all' ? undefined : parseInt(value);
    setFilters((prev) => ({ ...prev, is_active: isActive, page: 1 }));
  };

  /**
   * 削除
   */
  const handleDelete = async (id: number) => {
    if (!confirm('この商品を削除しますか？\n（論理削除されます）')) {
      return;
    }

    try {
      await deleteProduct(id);
      setSuccess('商品を削除しました');
      fetchProducts();
    } catch (err) {
      setError('商品の削除に失敗しました');
      console.error('Error deleting product:', err);
    }
  };

  /**
   * 価格フォーマット
   */
  const formatPrice = (price: number | null): string => {
    if (price === null) return '-';
    return new Intl.NumberFormat('ja-JP', {
      style: 'currency',
      currency: 'JPY',
    }).format(price);
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* ヘッダー */}
      <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <InventoryIcon sx={{ fontSize: 32, color: 'primary.main' }} />
          <Typography variant="h4" component="h1">
            商品マスタ
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => alert('商品作成機能は開発中です')}
        >
          新規商品登録
        </Button>
      </Box>

      {/* アラート */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* フィルター */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={5}>
            <TextField
              fullWidth
              label="検索（商品コード、商品名）"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              InputProps={{
                endAdornment: (
                  <IconButton onClick={handleSearch} edge="end">
                    <SearchIcon />
                  </IconButton>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              select
              fullWidth
              label="カテゴリ"
              value={filters.category || 'all'}
              onChange={(e) => handleCategoryChange(e.target.value)}
            >
              <MenuItem value="all">全て</MenuItem>
              {categories.map((cat) => (
                <MenuItem key={cat} value={cat}>
                  {cat}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} md={2}>
            <TextField
              select
              fullWidth
              label="ステータス"
              value={filters.is_active === undefined ? 'all' : filters.is_active.toString()}
              onChange={(e) => handleActiveFilterChange(e.target.value)}
            >
              <MenuItem value="all">全て</MenuItem>
              <MenuItem value="1">有効</MenuItem>
              <MenuItem value="0">無効</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} md={2}>
            <Typography variant="body2" color="text.secondary">
              全 {total} 件
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* テーブル */}
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : products.length === 0 ? (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography color="text.secondary">商品が見つかりませんでした</Typography>
          </Box>
        ) : (
          <Box sx={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#f5f5f5', borderBottom: '2px solid #ddd' }}>
                  <th style={{ padding: '12px', textAlign: 'left', fontWeight: 600 }}>商品コード</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontWeight: 600 }}>商品名</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontWeight: 600 }}>商品名（英語）</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontWeight: 600 }}>カテゴリ</th>
                  <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>標準単価</th>
                  <th style={{ padding: '12px', textAlign: 'center', fontWeight: 600 }}>単位</th>
                  <th style={{ padding: '12px', textAlign: 'center', fontWeight: 600 }}>ステータス</th>
                  <th style={{ padding: '12px', textAlign: 'center', fontWeight: 600 }}>アクション</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr
                    key={product.id}
                    style={{ borderBottom: '1px solid #eee' }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = '#f9f9f9';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = 'transparent';
                    }}
                  >
                    <td style={{ padding: '12px' }}>
                      <Typography variant="body2" fontWeight={500}>
                        {product.product_code}
                      </Typography>
                    </td>
                    <td style={{ padding: '12px' }}>
                      <Typography variant="body2">{product.product_name}</Typography>
                    </td>
                    <td style={{ padding: '12px' }}>
                      <Typography variant="body2" color="text.secondary">
                        {product.product_name_en || '-'}
                      </Typography>
                    </td>
                    <td style={{ padding: '12px' }}>
                      <Typography variant="body2">{product.category || '-'}</Typography>
                    </td>
                    <td style={{ padding: '12px', textAlign: 'right' }}>
                      <Typography variant="body2" fontWeight={500}>
                        {formatPrice(product.standard_price)}
                      </Typography>
                    </td>
                    <td style={{ padding: '12px', textAlign: 'center' }}>
                      <Typography variant="body2">{product.unit || '-'}</Typography>
                    </td>
                    <td style={{ padding: '12px', textAlign: 'center' }}>
                      <Chip
                        label={product.is_active === 1 ? '有効' : '無効'}
                        color={product.is_active === 1 ? 'success' : 'default'}
                        size="small"
                      />
                    </td>
                    <td style={{ padding: '12px', textAlign: 'center' }}>
                      <Stack direction="row" spacing={1} justifyContent="center">
                        <Tooltip title="編集">
                          <IconButton
                            size="small"
                            color="primary"
                            onClick={() => alert('編集機能は開発中です')}
                          >
                            <EditIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="削除">
                          <IconButton
                            size="small"
                            color="error"
                            onClick={() => handleDelete(product.id)}
                          >
                            <DeleteIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Stack>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Box>
        )}
      </Paper>

      {/* ページネーション */}
      {totalPages > 1 && (
        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={handlePageChange}
            color="primary"
            showFirstButton
            showLastButton
          />
        </Box>
      )}
    </Container>
  );
};
