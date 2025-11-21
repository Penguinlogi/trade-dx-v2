# Phase 2: 案件番号採番サーバー

## 概要
中央集権型の案件番号採番サーバーです。複数のクライアントから同時にアクセスしても、重複のない案件番号を生成できます。

## 機能
- HTTPサーバーとして動作
- 案件種別ごとの連番管理（EX, IM, TR, DO）
- スレッドセーフな案件番号生成
- 生成履歴の記録（最新100件）
- VBAクライアント対応
- ヘルスチェック機能

## ファイル構成
```
scripts/phase2/
├── case_number_server.py     # サーバー本体
├── start_server.bat           # サーバー起動スクリプト（Windows）
├── start_server.sh            # サーバー起動スクリプト（Linux/Mac）
├── GenerateCaseNumber.bas     # VBAクライアント
├── case_numbers.json          # データファイル（自動生成）
└── README.md                  # このファイル
```

## インストール

### 1. 必要なライブラリ
```bash
# requestsライブラリ（テスト用）
pip install requests
```

### 2. サーバーの起動

#### Windows
```batch
cd scripts/phase2
start_server.bat
```

#### Linux/Mac
```bash
cd scripts/phase2
chmod +x start_server.sh
./start_server.sh
```

#### コマンドライン
```bash
cd scripts/phase2
python case_number_server.py --host localhost --port 8080
```

サーバーが起動すると、以下のメッセージが表示されます：
```
============================================================
案件番号採番サーバーを起動します
ホスト: localhost
ポート: 8080
データファイル: ./case_numbers.json
============================================================

利用可能なエンドポイント:
  - http://localhost:8080/health
  - http://localhost:8080/status
  - http://localhost:8080/generate?type=EX&user=yamada

Ctrl+C で終了します
============================================================
```

## APIエンドポイント

### 1. ヘルスチェック
サーバーが正常に動作しているか確認します。

```
GET http://localhost:8080/health
```

**レスポンス:**
```json
{
  "success": true,
  "status": "healthy",
  "message": "サーバーは正常に動作しています",
  "timestamp": "2025-11-19T10:00:00"
}
```

### 2. 案件番号生成
新しい案件番号を生成します。

```
GET http://localhost:8080/generate?type=EX&user=yamada
```

**パラメータ:**
- `type`: 案件種別（EX, IM, TR, DO）※必須
- `user`: ユーザー名（任意、デフォルト: unknown）

**レスポンス（成功）:**
```json
{
  "success": true,
  "case_number": "EX-250001",
  "message": "案件番号を生成しました",
  "timestamp": "2025-11-19T10:00:00"
}
```

**レスポンス（失敗）:**
```json
{
  "success": false,
  "case_number": null,
  "message": "無効な案件種別です: XX"
}
```

### 3. ステータス取得
現在のカウンター状態と履歴を取得します。

```
GET http://localhost:8080/status
```

**レスポンス:**
```json
{
  "success": true,
  "counters": {
    "EX": {
      "counter": 5,
      "last_generated": "2025-11-19T10:00:00"
    },
    "IM": {
      "counter": 3,
      "last_generated": "2025-11-19T09:30:00"
    },
    ...
  },
  "history_count": 8,
  "latest_history": [...]
}
```

### 4. カウンターリセット（管理用）
カウンターをリセットします。

```
GET http://localhost:8080/reset?type=EX
```

**パラメータ:**
- `type`: リセットする案件種別（省略時は全てリセット）

## VBAクライアントの使い方

### 1. VBAモジュールのインポート
1. Excelファイルを開く
2. `Alt + F11` で VBE を開く
3. `ファイル` → `ファイルのインポート`
4. `GenerateCaseNumber.bas` を選択

### 2. 基本的な使い方

#### 案件番号の生成
```vba
Sub CreateNewCase()
    Dim caseNumber As String
    caseNumber = GenerateCaseNumberFromServer("EX", "山田")
    
    If caseNumber <> "" Then
        ' 成功：案件番号をセルに入力
        Range("A2").Value = caseNumber
    Else
        ' 失敗
        MsgBox "案件番号の生成に失敗しました"
    End If
End Sub
```

#### ヘルスチェック
```vba
Sub CheckServer()
    If CheckServerHealth() Then
        MsgBox "サーバーは正常です"
    Else
        MsgBox "サーバーに接続できません"
    End If
End Sub
```

#### ステータス表示
```vba
Sub ViewStatus()
    ShowServerStatus
End Sub
```

### 3. フォールバック機能
サーバーに接続できない場合、自動的にローカルで案件番号を生成します（重複の可能性あり）。

設定で無効化することも可能：
```vba
Private Const ENABLE_FALLBACK As Boolean = False
```

## テスト

### 単体テスト
```bash
cd scripts/tests
python -m pytest test_phase2.py -v -m "not integration"
```

### 統合テスト（サーバー起動が必要）
```bash
# ターミナル1: サーバーを起動
cd scripts/phase2
python case_number_server.py

# ターミナル2: テストを実行
cd scripts/tests
python -m pytest test_phase2.py -v -m integration
```

## ブラウザでのテスト
サーバーを起動後、ブラウザで以下のURLにアクセスできます：

- http://localhost:8080/health
- http://localhost:8080/status
- http://localhost:8080/generate?type=EX&user=test

## トラブルシューティング

### サーバーが起動しない
- Pythonがインストールされているか確認
- ポート8080が他のプログラムで使用されていないか確認
- ファイアウォールの設定を確認

### VBAから接続できない
- サーバーが起動しているか確認（ブラウザで http://localhost:8080/health にアクセス）
- Excel のマクロ設定を確認
- `MSXML2.XMLHTTP` が利用可能か確認

### 案件番号が重複する
- サーバーを複数起動していないか確認
- `case_numbers.json` ファイルが破損していないか確認
- 複数のデータファイルを使用していないか確認

## データファイル
案件番号のカウンターは `case_numbers.json` に保存されます。

**注意:** このファイルを手動で編集しないでください。破損の原因になります。

バックアップを取る場合：
```bash
cp case_numbers.json case_numbers_backup.json
```

## セキュリティ
このサーバーは開発環境での使用を想定しています。

本番環境で使用する場合は、以下の対策を検討してください：
- 認証機能の追加
- HTTPS対応
- アクセス制限
- ログ監視

## ログ
サーバーのログは以下に保存されます：
```
../../logs/case_number_server_YYYYMMDD.log
```

## 次のステップ
Phase 2が完了したら、Phase 3（差分同期機能）に進みます。

## お問い合わせ
問題が発生した場合は、以下を確認してください：
- ログファイル
- テスト結果
- サーバーのステータス


