/**
 * 顧客別売上TOP10テーブルコンポーネント
 */
import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
  Chip,
} from '@mui/material';
import { EmojiEvents } from '@mui/icons-material';
import type { CustomerRevenue } from '../../types/analytics';

interface TopCustomersTableProps {
  customers: CustomerRevenue[];
  limit?: number;
}

export const TopCustomersTable: React.FC<TopCustomersTableProps> = ({
  customers,
  limit = 10,
}) => {
  // ランクの色（アイコン用）
  const getRankIconColor = (rank: number): 'error' | 'warning' | 'info' | 'inherit' => {
    if (rank === 1) return 'error';
    if (rank === 2) return 'warning';
    if (rank === 3) return 'info';
    return 'inherit';
  };

  // ランクアイコン
  const RankIcon = ({ rank }: { rank: number }) => {
    if (rank <= 3) {
      return <EmojiEvents color={getRankIconColor(rank)} />;
    }
    const chipColor = rank <= 3 ? getRankIconColor(rank) : 'default';
    return (
      <Chip
        label={rank}
        size="small"
        color={chipColor === 'inherit' ? 'default' : chipColor}
        sx={{ width: 32, height: 32 }}
      />
    );
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          顧客別売上TOP{limit}
        </Typography>

        {customers.length === 0 ? (
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
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell align="center" sx={{ width: 60 }}>
                    順位
                  </TableCell>
                  <TableCell>顧客コード</TableCell>
                  <TableCell>顧客名</TableCell>
                  <TableCell align="right">案件数</TableCell>
                  <TableCell align="right">総売上額</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {customers.map((customer, index) => {
                  const rank = index + 1;
                  return (
                    <TableRow
                      key={customer.customer_id}
                      hover
                      sx={{
                        '&:nth-of-type(odd)': {
                          backgroundColor: 'action.hover',
                        },
                      }}
                    >
                      <TableCell align="center">
                        <Box
                          display="flex"
                          justifyContent="center"
                          alignItems="center"
                        >
                          <RankIcon rank={rank} />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" fontFamily="monospace">
                          {customer.customer_code}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" fontWeight="medium">
                          {customer.customer_name}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {customer.case_count}件
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography
                          variant="body2"
                          fontWeight="bold"
                          color={rank <= 3 ? 'primary' : 'inherit'}
                        >
                          ¥{customer.total_revenue.toLocaleString()}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        {/* 合計行 */}
        {customers.length > 0 && (
          <Box
            mt={2}
            p={1.5}
            bgcolor="grey.100"
            borderRadius={1}
            display="flex"
            justifyContent="space-between"
          >
            <Typography variant="body2" fontWeight="bold">
              合計
            </Typography>
            <Box display="flex" gap={4}>
              <Typography variant="body2" fontWeight="bold">
                案件数: {customers.reduce((sum, c) => sum + c.case_count, 0)}件
              </Typography>
              <Typography variant="body2" fontWeight="bold" color="primary">
                売上額: ¥
                {customers
                  .reduce((sum, c) => sum + c.total_revenue, 0)
                  .toLocaleString()}
              </Typography>
            </Box>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};
