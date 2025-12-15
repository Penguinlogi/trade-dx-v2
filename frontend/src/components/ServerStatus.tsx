/**
 * サーバー状態表示コンポーネント
 */
import React from 'react';
import { Box, Chip, Tooltip } from '@mui/material';
import {
  CloudDone,
  CloudOff,
  People,
  Sync,
} from '@mui/icons-material';
import { useWebSocket } from '../hooks/useWebSocket';
import { format } from 'date-fns';

interface ServerStatusProps {
  compact?: boolean;
}

export const ServerStatusIndicator: React.FC<ServerStatusProps> = ({ compact = false }) => {
  const { isConnected, serverStatus } = useWebSocket();

  const formatLastSync = (lastSync: string | null): string => {
    if (!lastSync) return '未同期';
    try {
      const date = new Date(lastSync);
      return format(date, 'yyyy/MM/dd HH:mm:ss');
    } catch {
      return '不明';
    }
  };

  if (compact) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Tooltip title={isConnected ? '接続中' : '切断中'}>
          <Chip
            icon={isConnected ? <CloudDone /> : <CloudOff />}
            label={isConnected ? 'オンライン' : 'オフライン'}
            color={isConnected ? 'success' : 'default'}
            size="small"
          />
        </Tooltip>
        {serverStatus && (
          <Tooltip title={`接続ユーザー数: ${serverStatus.connected_users}人${serverStatus.total_connections ? ` (全接続数: ${serverStatus.total_connections})` : ''}`}>
            <Chip
              icon={<People />}
              label={serverStatus.connected_users}
              size="small"
              variant="outlined"
            />
          </Tooltip>
        )}
      </Box>
    );
  }

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        gap: 2,
        p: 1,
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: 1,
        bgcolor: 'background.paper',
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Chip
          icon={isConnected ? <CloudDone /> : <CloudOff />}
          label={isConnected ? 'オンライン' : 'オフライン'}
          color={isConnected ? 'success' : 'default'}
          size="small"
        />
        {serverStatus && (
          <>
            <Tooltip title={`接続ユーザー数: ${serverStatus.connected_users}人${serverStatus.total_connections ? ` (全接続数: ${serverStatus.total_connections})` : ''}`}>
              <Chip
                icon={<People />}
                label={`${serverStatus.connected_users}人接続`}
                size="small"
                variant="outlined"
              />
            </Tooltip>
            <Tooltip title={`最終同期: ${formatLastSync(serverStatus.last_sync)}`}>
              <Chip
                icon={<Sync />}
                label={formatLastSync(serverStatus.last_sync)}
                size="small"
                variant="outlined"
              />
            </Tooltip>
          </>
        )}
      </Box>
    </Box>
  );
};
