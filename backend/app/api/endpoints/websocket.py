"""
WebSocketエンドポイント
リアルタイム通知機能を提供
"""
import json
import asyncio
from typing import Dict, Set, Optional
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from ...core.database import SessionLocal
from ...core.security import decode_access_token
from ...models.user import User as UserModel

router = APIRouter()

# 接続管理: {user_id: Set[WebSocket]}
active_connections: Dict[int, Set[WebSocket]] = {}

# サーバー状態
server_status = {
    "status": "online",
    "last_sync": None,
    "connected_users": 0,
}


def get_db():
    """データベースセッションを取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_from_token(token: Optional[str], db: Session) -> Optional[UserModel]:
    """WebSocket接続のトークンからユーザーを取得"""
    if not token:
        return None

    try:
        payload = decode_access_token(token)
        if payload is None:
            return None

        user_id = payload.get("sub")
        if user_id is None:
            return None

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        return user
    except Exception:
        return None


async def broadcast_message(message: dict, exclude_user_id: Optional[int] = None):
    """全接続にメッセージをブロードキャスト"""
    import logging
    disconnected = []

    total_connections = sum(len(conns) for conns in active_connections.values())
    logging.info(f"[WebSocket] ブロードキャスト送信: type={message.get('type')}, exclude_user_id={exclude_user_id}, total_connections={total_connections}")
    print(f"[WebSocket] ブロードキャスト送信: type={message.get('type')}, exclude_user_id={exclude_user_id}, total_connections={total_connections}")

    sent_count = 0
    for user_id, connections in active_connections.items():
        if exclude_user_id and user_id == exclude_user_id:
            logging.debug(f"[WebSocket] ユーザー {user_id} を除外")
            continue

        for connection in connections:
            try:
                await connection.send_json(message)
                sent_count += 1
                logging.debug(f"[WebSocket] メッセージを送信: user_id={user_id}")
            except Exception as e:
                logging.warning(f"[WebSocket] メッセージ送信エラー: user_id={user_id}, error={e}")
                print(f"[WebSocket] メッセージ送信エラー: user_id={user_id}, error={e}")
                disconnected.append((user_id, connection))

    logging.info(f"[WebSocket] ブロードキャスト完了: {sent_count}件送信")
    print(f"[WebSocket] ブロードキャスト完了: {sent_count}件送信")

    # 切断された接続を削除
    for user_id, connection in disconnected:
        active_connections[user_id].discard(connection)
        if not active_connections[user_id]:
            del active_connections[user_id]


async def send_to_user(user_id: int, message: dict):
    """特定のユーザーにメッセージを送信"""
    if user_id not in active_connections:
        return

    disconnected = []
    for connection in active_connections[user_id]:
        try:
            await connection.send_json(message)
        except Exception:
            disconnected.append(connection)

    # 切断された接続を削除
    for connection in disconnected:
        active_connections[user_id].discard(connection)

    if not active_connections[user_id]:
        del active_connections[user_id]


def update_server_status():
    """サーバー状態を更新"""
    server_status["last_sync"] = datetime.now().isoformat()
    # 接続数（全接続の合計）
    total_connections = sum(len(conns) for conns in active_connections.values())
    # ユーザー数（接続しているユーザーの数）
    unique_users = len(active_connections)
    server_status["connected_users"] = unique_users  # ユーザー数を表示
    server_status["total_connections"] = total_connections  # 接続数も記録（デバッグ用）


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    """
    WebSocketエンドポイント
    リアルタイム通知を受信する

    Args:
        websocket: WebSocket接続
        token: JWT認証トークン（クエリパラメータ）
    """
    await websocket.accept()
    user: Optional[UserModel] = None
    user_id: Optional[int] = None

    try:
        # トークンからユーザーを取得
        db = SessionLocal()
        try:
            user = await get_user_from_token(token, db)
        finally:
            db.close()

        if not user or not user.is_active:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        user_id = user.id

        # 接続を登録
        if user_id not in active_connections:
            active_connections[user_id] = set()
        active_connections[user_id].add(websocket)

        # サーバー状態を更新
        update_server_status()

        # 接続成功メッセージを送信
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
            },
            "server_status": server_status,
        })

        # 他のユーザーに接続通知を送信
        await broadcast_message({
            "type": "user_connected",
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
            },
            "server_status": server_status,
        }, exclude_user_id=user_id)

        # メッセージ受信ループ
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)

                # ハートビート（接続維持）
                if message.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat(),
                    })

                # サーバー状態取得リクエスト
                elif message.get("type") == "get_status":
                    update_server_status()
                    await websocket.send_json({
                        "type": "server_status",
                        "status": server_status,
                    })

            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "無効なJSON形式です",
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"エラーが発生しました: {str(e)}",
                })

    except Exception as e:
        print(f"WebSocketエラー: {e}")

    finally:
        # 接続を解除
        if user_id and user_id in active_connections:
            active_connections[user_id].discard(websocket)
            remaining_connections = len(active_connections[user_id])
            if not active_connections[user_id]:
                del active_connections[user_id]
            import logging
            logging.info(f"[WebSocket] 接続を解除: user_id={user_id}, 残り接続数={remaining_connections}")

        # サーバー状態を更新
        update_server_status()

        # 他のユーザーに切断通知を送信（ユーザーの全接続が切れた場合のみ）
        if user_id and user_id not in active_connections:
            await broadcast_message({
                "type": "user_disconnected",
                "user": {
                    "id": user.id if user else None,
                    "username": user.username if user else None,
                },
                "server_status": server_status,
            }, exclude_user_id=user_id)


# リアルタイム通知を送信する関数（他のモジュールから呼び出し可能）
async def notify_case_updated(case_id: int, action: str, user_id: Optional[int] = None):
    """案件更新通知を送信"""
    import logging
    update_server_status()
    message = {
        "type": "case_updated",
        "case_id": case_id,
        "action": action,  # "created", "updated", "deleted"
        "timestamp": datetime.now().isoformat(),
        "server_status": server_status,
    }
    total_connections = sum(len(conns) for conns in active_connections.values())
    logging.info(f"[WebSocket] 通知を送信: case_updated, case_id={case_id}, action={action}, user_id={user_id}, active_connections={total_connections}")
    print(f"[WebSocket] 通知を送信: case_updated, case_id={case_id}, action={action}, user_id={user_id}, active_connections={total_connections}")
    await broadcast_message(message, exclude_user_id=user_id)


async def notify_customer_updated(customer_id: int, action: str, user_id: Optional[int] = None):
    """顧客マスタ更新通知を送信"""
    update_server_status()
    await broadcast_message({
        "type": "customer_updated",
        "customer_id": customer_id,
        "action": action,
        "timestamp": datetime.now().isoformat(),
        "server_status": server_status,
    })


async def notify_product_updated(product_id: int, action: str, user_id: Optional[int] = None):
    """商品マスタ更新通知を送信"""
    update_server_status()
    await broadcast_message({
        "type": "product_updated",
        "product_id": product_id,
        "action": action,
        "timestamp": datetime.now().isoformat(),
        "server_status": server_status,
    })


async def notify_document_generated(document_id: int, case_id: int, document_type: str, user_id: Optional[int] = None):
    """ドキュメント生成通知を送信"""
    update_server_status()
    await broadcast_message({
        "type": "document_generated",
        "document_id": document_id,
        "case_id": case_id,
        "document_type": document_type,
        "timestamp": datetime.now().isoformat(),
        "server_status": server_status,
    })


async def notify_backup_created(backup_id: int, user_id: Optional[int] = None):
    """バックアップ作成通知を送信"""
    update_server_status()
    await broadcast_message({
        "type": "backup_created",
        "backup_id": backup_id,
        "timestamp": datetime.now().isoformat(),
        "server_status": server_status,
    })
