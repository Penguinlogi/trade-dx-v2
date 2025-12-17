/**
 * ステータス分布チャートコンポーネント
 */
import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import type { CaseStatusDistribution } from '../../types/analytics';

interface StatusDistributionChartProps {
  distribution: CaseStatusDistribution[];
}

// ステータスごとの色
const STATUS_COLORS: Record<string, string> = {
  見積中: '#2196f3',
  受注済: '#ff9800',
  船積済: '#9c27b0',
  完了: '#4caf50',
  キャンセル: '#f44336',
};

export const StatusDistributionChart: React.FC<StatusDistributionChartProps> = ({
  distribution,
}) => {
  // rechartsのデータ形式に変換
  const chartData = distribution.map((item) => ({
    name: item.status,
    value: item.count,
    percentage: item.percentage,
  }));

  // カスタムラベル
  const renderLabel = (entry: any) => {
    return `${entry.percentage.toFixed(1)}%`;
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          案件ステータス分布
        </Typography>

        {distribution.length === 0 ? (
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
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={renderLabel}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={STATUS_COLORS[entry.name] || '#999999'}
                  />
                ))}
              </Pie>
              <Tooltip
                formatter={(value: number, name: string, props: any) => [
                  `${value}件 (${props.payload.percentage.toFixed(1)}%)`,
                  name,
                ]}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        )}

        {/* 統計情報 */}
        <Box mt={2}>
          {distribution.map((item) => (
            <Box
              key={item.status}
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              mb={1}
            >
              <Box display="flex" alignItems="center">
                <Box
                  sx={{
                    width: 16,
                    height: 16,
                    borderRadius: '50%',
                    bgcolor: STATUS_COLORS[item.status] || '#999999',
                    mr: 1,
                  }}
                />
                <Typography variant="body2">{item.status}</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                {item.count}件 ({item.percentage.toFixed(1)}%)
              </Typography>
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
};







