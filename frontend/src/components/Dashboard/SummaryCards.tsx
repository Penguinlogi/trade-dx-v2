/**
 * サマリーカードコンポーネント
 */
import React from 'react';
import { Grid, Card, CardContent, Typography, Box } from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Description,
  CheckCircle,
  People,
  Inventory,
} from '@mui/icons-material';
import type { SummaryData } from '../../types/analytics';

interface SummaryCardsProps {
  summary: SummaryData;
}

export const SummaryCards: React.FC<SummaryCardsProps> = ({ summary }) => {
  // 売上の増減率を計算
  const revenueChange =
    summary.last_month_revenue > 0
      ? ((summary.this_month_revenue - summary.last_month_revenue) / summary.last_month_revenue) * 100
      : 0;

  const isRevenueUp = revenueChange >= 0;

  const cards = [
    {
      title: '総案件数',
      value: summary.total_cases,
      icon: <Description sx={{ fontSize: 40, color: 'primary.main' }} />,
      color: '#1976d2',
    },
    {
      title: '進行中案件',
      value: summary.active_cases,
      icon: <TrendingUp sx={{ fontSize: 40, color: 'warning.main' }} />,
      color: '#ed6c02',
    },
    {
      title: '完了案件',
      value: summary.completed_cases,
      icon: <CheckCircle sx={{ fontSize: 40, color: 'success.main' }} />,
      color: '#2e7d32',
    },
    {
      title: '顧客数',
      value: summary.total_customers,
      icon: <People sx={{ fontSize: 40, color: 'info.main' }} />,
      color: '#0288d1',
    },
    {
      title: '商品数',
      value: summary.total_products,
      icon: <Inventory sx={{ fontSize: 40, color: 'secondary.main' }} />,
      color: '#9c27b0',
    },
    {
      title: '今月の案件数',
      value: summary.this_month_cases,
      icon: <Description sx={{ fontSize: 40, color: 'primary.main' }} />,
      color: '#1976d2',
    },
  ];

  return (
    <Grid container spacing={3}>
      {cards.map((card, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {card.title}
                  </Typography>
                  <Typography variant="h4" component="div">
                    {card.value.toLocaleString()}
                  </Typography>
                </Box>
                {card.icon}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}

      {/* 今月の売上額 */}
      <Grid item xs={12} sm={6} md={6}>
        <Card sx={{ height: '100%', bgcolor: 'success.light' }}>
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Box>
                <Typography variant="body2" color="success.dark" gutterBottom>
                  今月の売上額
                </Typography>
                <Typography variant="h4" component="div" color="success.dark">
                  ¥{summary.this_month_revenue.toLocaleString()}
                </Typography>
                <Box display="flex" alignItems="center" mt={1}>
                  {isRevenueUp ? (
                    <TrendingUp color="success" sx={{ mr: 0.5 }} />
                  ) : (
                    <TrendingDown color="error" sx={{ mr: 0.5 }} />
                  )}
                  <Typography
                    variant="body2"
                    color={isRevenueUp ? 'success.dark' : 'error.main'}
                  >
                    {isRevenueUp ? '+' : ''}
                    {revenueChange.toFixed(1)}% 前月比
                  </Typography>
                </Box>
              </Box>
              <TrendingUp sx={{ fontSize: 40, color: 'success.dark' }} />
            </Box>
          </CardContent>
        </Card>
      </Grid>

      {/* 先月の売上額 */}
      <Grid item xs={12} sm={6} md={6}>
        <Card sx={{ height: '100%', bgcolor: 'info.light' }}>
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Box>
                <Typography variant="body2" color="info.dark" gutterBottom>
                  先月の売上額
                </Typography>
                <Typography variant="h4" component="div" color="info.dark">
                  ¥{summary.last_month_revenue.toLocaleString()}
                </Typography>
              </Box>
              <TrendingUp sx={{ fontSize: 40, color: 'info.dark' }} />
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};





