/**
 * WebSocket接続管理フック
 */
import { useEffect, useRef, useState, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';

// WebSocketメッセージの型定義
export interface WebSocketMessage {
  type: string;
  [key: string]: any;
}

export interface ServerStatus {
  status: string;
  last_sync: string | null;
  connected_users: number;  // 接続しているユーザー数
  total_connections?: number;  // 全接続数（デバッグ用）
}

export interface WebSocketHookReturn {
  isConnected: boolean;
  serverStatus: ServerStatus | null;
  sendMessage: (message: WebSocketMessage) => void;
  lastMessage: WebSocketMessage | null;
}

// WebSocket URLを取得
const getWebSocketUrl = (): string => {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  const wsProtocol = apiBaseUrl.startsWith('https') ? 'wss' : 'ws';
  const wsUrl = apiBaseUrl.replace(/^https?:\/\//, '');
  const token = localStorage.getItem('access_token');
  return `${wsProtocol}://${wsUrl}/api/ws${token ? `?token=${token}` : ''}`;
};

/**
 * WebSocket接続を管理するフック
 */
export const useWebSocket = (): WebSocketHookReturn => {
  const { isAuthenticated } = useAuth();
  const [isConnected, setIsConnected] = useState(false);
  const [serverStatus, setServerStatus] = useState<ServerStatus | null>(null);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  type TimeoutRef = ReturnType<typeof setTimeout> | null;
  const reconnectTimeoutRef = useRef<TimeoutRef>(null);
  const pingIntervalRef = useRef<TimeoutRef>(null);
  const pongTimeoutRef = useRef<TimeoutRef>(null);
  const lastPongTimeRef = useRef<number>(Date.now());

  // メッセージ送信
  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  // WebSocket接続
  const connect = useCallback(() => {
    if (!isAuthenticated) {
      return;
    }

    // 既に接続中または接続済みの場合は何もしない
    if (wsRef.current) {
      if (wsRef.current.readyState === WebSocket.OPEN) {
        return;
      }
      if (wsRef.current.readyState === WebSocket.CONNECTING) {
        return;
      }
      // 閉じている接続は削除
      if (wsRef.current.readyState === WebSocket.CLOSED) {
        wsRef.current = null;
      }
    }

    try {
      const wsUrl = getWebSocketUrl();
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        console.log('WebSocket接続が確立されました');
        setIsConnected(true);
        lastPongTimeRef.current = Date.now();

        // ハートビート（30秒ごと）
        pingIntervalRef.current = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            // 前回のpongから時間が経過している場合は警告
            const timeSinceLastPong = Date.now() - lastPongTimeRef.current;
            if (timeSinceLastPong > 60000) {
              console.warn('[useWebSocket] ハートビート: 前回のpongから60秒以上経過しています。接続が切断された可能性があります。');
              setIsConnected(false);
              setServerStatus(null);
              if (wsRef.current) {
                wsRef.current.close();
              }
              return;
            }

            sendMessage({ type: 'ping' });

            // pongのタイムアウトを監視（30秒以内にpongが来ない場合は切断とみなす）
            if (pongTimeoutRef.current) {
              clearTimeout(pongTimeoutRef.current);
            }
            pongTimeoutRef.current = setTimeout(() => {
              const timeSinceLastPong = Date.now() - lastPongTimeRef.current;
              if (timeSinceLastPong > 30000) {
                console.warn('[useWebSocket] ハートビートタイムアウト: ping送信後30秒以内にpongが来ませんでした。接続が切断された可能性があります。');
                setIsConnected(false);
                setServerStatus(null);
                // 接続を閉じる
                if (wsRef.current) {
                  wsRef.current.close();
                }
              }
            }, 30000); // 30秒でタイムアウト
          }
        }, 30000);
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          console.log('WebSocket useWebSocket.ts:93 メッセージを受信:', message);
          setLastMessage(message);

          // メッセージタイプに応じた処理
          switch (message.type) {
            case 'connection':
              if (message.server_status) {
                setServerStatus(message.server_status);
              }
              break;
            case 'server_status':
              if (message.status) {
                setServerStatus(message.status);
              }
              break;
            case 'pong':
              // ハートビート応答
              lastPongTimeRef.current = Date.now();
              if (pongTimeoutRef.current) {
                clearTimeout(pongTimeoutRef.current);
                pongTimeoutRef.current = null;
              }
              break;
            case 'user_connected':
            case 'user_disconnected':
              if (message.server_status) {
                setServerStatus(message.server_status);
              }
              // 接続・切断通知イベントを発火
              window.dispatchEvent(
                new CustomEvent('websocket:update', { detail: message })
              );
              break;
            case 'case_updated':
            case 'customer_updated':
            case 'product_updated':
            case 'document_generated':
            case 'backup_created':
              if (message.server_status) {
                setServerStatus(message.server_status);
              }
              // リアルタイム更新イベントを発火
              window.dispatchEvent(
                new CustomEvent('websocket:update', { detail: message })
              );
              break;
            case 'error':
              console.error('WebSocketエラー:', message.message);
              break;
            default:
              console.log('未処理のWebSocketメッセージ:', message);
          }
        } catch (error) {
          console.error('WebSocketメッセージの解析エラー:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocketエラー:', error);
        // ネットワーク切断時は即座にオフラインに切り替え
        // 開発モードでも、接続済みの状態でのエラーは無視しない
        if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
          setIsConnected(false);
          setServerStatus(null);
        }
      };

      ws.onclose = (event) => {
        console.log('WebSocket接続が切断されました', {
          code: event.code,
          reason: event.reason,
          wasClean: event.wasClean,
        });
        setIsConnected(false);
        setServerStatus(null);

        // ハートビートを停止
        if (pingIntervalRef.current) {
          clearInterval(pingIntervalRef.current);
          pingIntervalRef.current = null;
        }

        // pongタイムアウトを停止
        if (pongTimeoutRef.current) {
          clearTimeout(pongTimeoutRef.current);
          pongTimeoutRef.current = null;
        }

        // 再接続（認証されている場合のみ）
        if (isAuthenticated) {
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, 3000);
        }
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('WebSocket接続エラー:', error);
      setIsConnected(false);
    }
  }, [isAuthenticated, sendMessage]);

  // 切断
  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (pingIntervalRef.current) {
      clearInterval(pingIntervalRef.current);
      pingIntervalRef.current = null;
    }

    if (pongTimeoutRef.current) {
      clearTimeout(pongTimeoutRef.current);
      pongTimeoutRef.current = null;
    }

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setIsConnected(false);
    setServerStatus(null);
  }, []);

  // 認証状態に応じて接続/切断
  useEffect(() => {
    if (!isAuthenticated) {
      disconnect();
      return;
    }

    // 接続を少し遅延させて、React StrictModeの二重レンダリングを防ぐ
    const connectTimer = setTimeout(() => {
      // 既に接続済みの場合は何もしない
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        console.log('[useWebSocket] 既に接続済みのため、新しい接続を作成しません');
        return;
      }
      connect();
    }, 200);  // 遅延を200msに増やして、二重レンダリングを確実に防ぐ

    return () => {
      clearTimeout(connectTimer);
      // クリーンアップ時は切断しない（React StrictModeの二重レンダリングを考慮）
      // 実際のアンマウント時のみ切断
    };
  }, [isAuthenticated, connect, disconnect]);

  // サーバー状態を定期的に取得
  useEffect(() => {
    if (!isConnected) return;

    const statusInterval = setInterval(() => {
      sendMessage({ type: 'get_status' });
    }, 60000); // 60秒ごと

    return () => {
      clearInterval(statusInterval);
    };
  }, [isConnected, sendMessage]);

  // ネットワーク状態の監視（navigator.onLine APIを使用）
  useEffect(() => {
    const handleOnline = () => {
      console.log('[useWebSocket] ネットワーク接続が復旧しました');
      // 接続が切れている場合は再接続を試みる
      if (!isConnected && isAuthenticated) {
        setTimeout(() => {
          connect();
        }, 1000);
      }
    };

    const handleOffline = () => {
      console.log('[useWebSocket] ネットワーク接続が切断されました');
      setIsConnected(false);
      setServerStatus(null);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // 初回チェック
    if (!navigator.onLine) {
      console.log('[useWebSocket] 初回チェック: オフライン状態');
      setIsConnected(false);
      setServerStatus(null);
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [isConnected, isAuthenticated, connect]);

  // WebSocket接続状態の定期チェック
  useEffect(() => {
    if (!isConnected || !isAuthenticated) {
      return;
    }

    const checkInterval = setInterval(() => {
      if (wsRef.current) {
        // WebSocket接続状態をチェック
        if (wsRef.current.readyState === WebSocket.CLOSED || wsRef.current.readyState === WebSocket.CLOSING) {
          console.log('[useWebSocket] 定期チェック: WebSocket接続が切断されています');
          setIsConnected(false);
          setServerStatus(null);
        } else if (wsRef.current.readyState === WebSocket.OPEN) {
          // 接続は開いているが、最後のpongから時間が経過している場合は切断とみなす
          const timeSinceLastPong = Date.now() - lastPongTimeRef.current;
          if (timeSinceLastPong > 90000) { // 90秒以上pongが来ない場合は切断
            console.warn('[useWebSocket] 定期チェック: pongの応答が90秒以上ありません。接続が切断された可能性があります。');
            setIsConnected(false);
            setServerStatus(null);
            if (wsRef.current) {
              wsRef.current.close();
            }
          }
        }
      } else {
        // WebSocket参照がない場合は切断状態
        setIsConnected(false);
        setServerStatus(null);
      }
    }, 10000); // 10秒ごとにチェック

    return () => {
      clearInterval(checkInterval);
    };
  }, [isConnected, isAuthenticated]);

  return {
    isConnected,
    serverStatus,
    sendMessage,
    lastMessage,
  };
};
