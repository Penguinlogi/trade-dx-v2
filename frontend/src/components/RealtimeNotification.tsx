/**
 * リアルタイム更新通知コンポーネント
 */
import React, { useEffect, useState } from 'react';
import { Snackbar, Alert, AlertColor } from '@mui/material';
import { useWebSocket, WebSocketMessage } from '../hooks/useWebSocket';

interface NotificationState {
  open: boolean;
  message: string;
  severity: AlertColor;
}

export const RealtimeNotification: React.FC = () => {
  const { lastMessage } = useWebSocket();
  const [notification, setNotification] = useState<NotificationState>({
    open: false,
    message: '',
    severity: 'info',
  });

  useEffect(() => {
    if (!lastMessage) {
      console.log('[RealtimeNotification] lastMessage is null');
      return;
    }

    console.log('[RealtimeNotification] lastMessageが更新されました:', lastMessage);

    const handleUpdate = (message: WebSocketMessage) => {
      console.log('[RealtimeNotification] handleUpdate called:', message);
      let notificationMessage = '';
      let severity: AlertColor = 'info';

      switch (message.type) {
        case 'case_updated':
          const actionMap: Record<string, string> = {
            created: '作成',
            updated: '更新',
            deleted: '削除',
          };
          notificationMessage = `案件が${actionMap[message.action] || '更新'}されました`;
          severity = 'success';
          break;
        case 'customer_updated':
          notificationMessage = `顧客マスタが${message.action === 'created' ? '追加' : message.action === 'updated' ? '更新' : '削除'}されました`;
          severity = 'info';
          break;
        case 'product_updated':
          notificationMessage = `商品マスタが${message.action === 'created' ? '追加' : message.action === 'updated' ? '更新' : '削除'}されました`;
          severity = 'info';
          break;
        case 'document_generated':
          notificationMessage = `ドキュメントが生成されました`;
          severity = 'success';
          break;
        case 'backup_created':
          notificationMessage = `バックアップが作成されました`;
          severity = 'info';
          break;
        case 'user_connected':
          notificationMessage = `${message.user?.username || 'ユーザー'}が接続しました`;
          severity = 'info';
          break;
        case 'user_disconnected':
          notificationMessage = `${message.user?.username || 'ユーザー'}が切断しました`;
          severity = 'info';
          break;
        default:
          return; // 通知不要なメッセージ
      }

      setNotification({
        open: true,
        message: notificationMessage,
        severity,
      });
    };

    // カスタムイベントをリッスン
    const handleCustomEvent = (event: CustomEvent) => {
      handleUpdate(event.detail);
    };

    window.addEventListener('websocket:update', handleCustomEvent as EventListener);

    // 直接メッセージを処理（カスタムイベントが発火しない場合）
    if (['case_updated', 'customer_updated', 'product_updated', 'document_generated', 'backup_created', 'user_connected', 'user_disconnected'].includes(lastMessage.type)) {
      handleUpdate(lastMessage);
    }

    return () => {
      window.removeEventListener('websocket:update', handleCustomEvent as EventListener);
    };
  }, [lastMessage]);

  const handleClose = () => {
    setNotification((prev) => ({ ...prev, open: false }));
  };

  return (
    <Snackbar
      open={notification.open}
      autoHideDuration={5000}
      onClose={handleClose}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
    >
      <Alert onClose={handleClose} severity={notification.severity} sx={{ width: '100%' }}>
        {notification.message}
      </Alert>
    </Snackbar>
  );
};
