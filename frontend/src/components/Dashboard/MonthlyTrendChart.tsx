/**
 * 月次トレンドチャートコンポーネント
 */
import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import type { MonthlyTrend } from '../../types/analytics';

interface MonthlyTrendChartProps {
  trends: MonthlyTrend[];
  periodMonths?: number;
}

export const MonthlyTrendChart: React.FC<MonthlyTrendChartProps> = ({
  trends,
  periodMonths = 12,
}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          月次トレンド（{periodMonths}ヶ月）
        </Typography>

        {trends.length === 0 ? (
          <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight={300}
          >
            <Typography variant="body2" color="text.secondary">
              データがありません
            </Typography>
          </Box>
        ) : (
          <>
            {/* 案件数の折れ線グラフ */}
            <Box mb={3}>
              <Typography variant="subtitle2" gutterBottom>
                案件数推移
              </Typography>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={trends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="year_month"
                    tick={{ fontSize: 12 }}
                    angle={-45}
                    textAnchor="end"
                    height={60}
                  />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="case_count"
                    name="案件数"
                    stroke="#1976d2"
                    strokeWidth={2}
                    dot={{ r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>

            {/* 売上額の棒グラフ */}
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                売上額推移
              </Typography>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={trends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="year_month"
                    tick={{ fontSize: 12 }}
                    angle={-45}
                    textAnchor="end"
                    height={60}
                  />
                  <YAxis
                    tickFormatter={(value) => `¥${(value / 1000000).toFixed(1)}M`}
                  />
                  <Tooltip
                    formatter={(value: number) => [`¥${value.toLocaleString()}`, '売上額']}
                  />
                  <Legend />
                  <Bar dataKey="revenue" name="売上額" fill="#9c27b0" />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </>
        )}
      </CardContent>
    </Card>
  );
};
