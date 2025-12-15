# VPS/クラウドVM セットアップガイド

## 📋 目次
1. [VPS/クラウドサービスの選定](#vpsクラウドサービスの選定)
2. [サーバー契約・アカウント作成](#サーバー契約アカウント作成)
3. [サーバーインスタンスの作成](#サーバーインスタンスの作成)
4. [初期セットアップ（OS設定）](#初期セットアップos設定)
5. [必要なソフトウェアのインストール](#必要なソフトウェアのインストール)
6. [セキュリティ設定](#セキュリティ設定)
7. [次のステップ](#次のステップ)

---

## 🎯 VPS/クラウドサービスの選定

### 推奨サービス一覧

#### 日本のVPSサービス（初心者向け・日本語サポートあり）

1. **さくらのVPS**
   - **料金**: 月額 1,100円〜（最小プラン）
   - **特徴**: 日本語サポート充実、初心者向け
   - **URL**: https://vps.sakura.ad.jp/
   - **推奨プラン**: 2GBメモリプラン（月額約2,200円）

2. **ConoHa VPS**
   - **料金**: 月額 900円〜（最小プラン）
   - **特徴**: 低価格、使いやすい管理画面
   - **URL**: https://www.conoha.jp/vps/
   - **推奨プラン**: 2GBメモリプラン（月額約1,200円）

3. **AWS（Amazon Web Services）**
   - **料金**: 従量課金（無料枠あり）
   - **特徴**: 世界最大のクラウドサービス、高機能
   - **URL**: https://aws.amazon.com/jp/
   - **推奨**: EC2 t3.micro（無料枠内で利用可能）

4. **Google Cloud Platform（GCP）**
   - **料金**: 従量課金（無料枠あり）
   - **特徴**: Googleのインフラ、高性能
   - **URL**: https://cloud.google.com/
   - **推奨**: e2-micro（無料枠内で利用可能）

#### 海外VPSサービス（低価格・高性能）

5. **Vultr**
   - **料金**: 月額 $6〜（約900円）
   - **特徴**: 低価格、高性能、日本リージョンあり
   - **URL**: https://www.vultr.com/

6. **DigitalOcean**
   - **料金**: 月額 $6〜（約900円）
   - **特徴**: 開発者向け、ドキュメント充実
   - **URL**: https://www.digitalocean.com/

### 選定のポイント

#### 初心者の方におすすめ
- ✅ **さくらのVPS** または **ConoHa VPS**
  - 日本語サポートあり
  - 管理画面がわかりやすい
  - 初期費用なし、月額課金のみ

#### コスト重視の方
- ✅ **AWS EC2** または **GCP e2-micro**（無料枠利用）
- ✅ **Vultr** または **DigitalOcean**（低価格）

#### 本番運用重視の方
- ✅ **AWS** または **GCP**（高可用性、スケーラビリティ）

### 推奨サーバー仕様

#### 最小構成（小規模運用・10ユーザー以下）
- **CPU**: 1コア
- **メモリ**: 2GB
- **ストレージ**: 20GB SSD
- **OS**: Ubuntu 22.04 LTS（推奨）

#### 推奨構成（中規模運用・10-50ユーザー）
- **CPU**: 2コア
- **メモリ**: 4GB
- **ストレージ**: 40GB SSD
- **OS**: Ubuntu 22.04 LTS（推奨）

#### 大規模構成（50ユーザー以上）
- **CPU**: 4コア以上
- **メモリ**: 8GB以上
- **ストレージ**: 80GB SSD以上
- **OS**: Ubuntu 22.04 LTS（推奨）

---

## 📝 サーバー契約・アカウント作成

### さくらのVPSの場合

1. **アカウント作成**
   - https://vps.sakura.ad.jp/ にアクセス
   - 「無料お試し」または「新規登録」をクリック
   - メールアドレス、パスワードを入力して登録

2. **サーバー作成**
   - コントロールパネルにログイン
   - 「サーバー追加」をクリック
   - プランを選択（推奨: 2GBメモリプラン）
   - OSを選択（Ubuntu 22.04 LTS推奨）
   - サーバー名を入力（例: `trade-dx-prod`）
   - 「作成」をクリック

3. **初期パスワードの確認**
   - サーバー作成後、初期パスワードが表示されます
   - **重要**: パスワードを必ずメモしてください

### ConoHa VPSの場合

1. **アカウント作成**
   - https://www.conoha.jp/vps/ にアクセス
   - 「無料お試し」をクリック
   - メールアドレス、パスワードを入力して登録

2. **サーバー作成**
   - コントロールパネルにログイン
   - 「VPS追加」をクリック
   - プランを選択（推奨: 2GBメモリプラン）
   - OSを選択（Ubuntu 22.04 LTS推奨）
   - サーバー名を入力（例: `trade-dx-prod`）
   - 「作成」をクリック

3. **初期パスワードの確認**
   - サーバー作成後、初期パスワードが表示されます
   - **重要**: パスワードを必ずメモしてください

### AWS EC2の場合

1. **AWSアカウント作成**
   - https://aws.amazon.com/jp/ にアクセス
   - 「AWSアカウントを作成」をクリック
   - メールアドレス、パスワードを入力して登録
   - クレジットカード情報を入力（無料枠利用時も必要）

2. **EC2インスタンス作成**
   - AWSコンソールにログイン
   - 「EC2」サービスを選択
   - 「インスタンスを起動」をクリック
   - OSを選択（Ubuntu Server 22.04 LTS推奨）
   - インスタンスタイプを選択（t3.micro推奨、無料枠）
   - キーペアを作成（SSH接続用）
   - 「インスタンスを起動」をクリック

3. **セキュリティグループ設定**
   - SSH（ポート22）を許可
   - HTTP（ポート80）を許可
   - HTTPS（ポート443）を許可
   - カスタムTCP（ポート8000）を許可（バックエンドAPI用）

---

## 🖥️ サーバーインスタンスの作成

### サーバー情報の記録

サーバー作成後、以下の情報を必ず記録してください：

| 項目 | 値 | 備考 |
|------|-----|------|
| **サーバーIPアドレス** | `xxx.xxx.xxx.xxx` | 例: 133.242.xxx.xxx |
| **SSHポート** | `22` | 通常は22 |
| **初期ユーザー名** | `root` または `ubuntu` | OSによって異なる |
| **初期パスワード** | `********` | サーバー作成時に表示 |
| **SSHキー** | `~/.ssh/id_rsa` | AWS等で使用 |

### サーバー接続確認

#### Windowsの場合（PowerShellまたはコマンドプロンプト）

```powershell
# SSH接続テスト
ssh root@サーバーIPアドレス
# または
ssh ubuntu@サーバーIPアドレス

# 初回接続時は「yes」を入力
# パスワードを入力
```

#### Mac/Linuxの場合

```bash
# SSH接続テスト
ssh root@サーバーIPアドレス
# または
ssh ubuntu@サーバーIPアドレス

# 初回接続時は「yes」を入力
# パスワードを入力
```

**接続できない場合の確認事項**:
- サーバーIPアドレスが正しいか
- ファイアウォールでSSH（ポート22）が許可されているか
- サーバーが起動しているか（コントロールパネルで確認）

---

## ⚙️ 初期セットアップ（OS設定）

### 1. システムアップデート

```bash
# Ubuntu/Debianの場合
sudo apt update
sudo apt upgrade -y

# 再起動（必要に応じて）
sudo reboot
```

### 2. タイムゾーンの設定

```bash
# 日本時間に設定
sudo timedatectl set-timezone Asia/Tokyo

# 確認
timedatectl
```

### 3. ファイアウォール設定（UFW）

```bash
# UFWのインストール（未インストールの場合）
sudo apt install ufw -y

# 基本設定
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 必要なポートを開放
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8000/tcp  # バックエンドAPI（開発用）

# ファイアウォールを有効化
sudo ufw enable

# 状態確認
sudo ufw status
```

### 4. ユーザー作成（root以外で運用する場合）

```bash
# 新しいユーザーを作成
sudo adduser trade-dx

# sudo権限を付与
sudo usermod -aG sudo trade-dx

# ユーザーを切り替え
su - trade-dx
```

---

## 📦 必要なソフトウェアのインストール

### 1. Python 3.11+ のインストール

```bash
# システムのPythonバージョンを確認
python3 --version

# Python 3.11以上がインストールされていない場合
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# pipのインストール
sudo apt install python3-pip -y

# 確認
python3.11 --version
pip3 --version
```

### 2. Node.js 18+ のインストール

```bash
# NodeSourceリポジトリを追加
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# Node.jsをインストール
sudo apt install -y nodejs

# 確認
node --version
npm --version
```

### 3. PostgreSQL 15+ のインストール（オプション）

```bash
# PostgreSQLリポジトリを追加
sudo apt install wget ca-certificates -y
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt update

# PostgreSQLをインストール
sudo apt install postgresql-15 postgresql-contrib-15 -y

# PostgreSQLを起動
sudo systemctl start postgresql
sudo systemctl enable postgresql

# データベースユーザーとデータベースを作成
sudo -u postgres psql
```

PostgreSQL内で実行:
```sql
-- データベースユーザーを作成
CREATE USER trade_dx_user WITH PASSWORD '強力なパスワード';

-- データベースを作成
CREATE DATABASE trade_dx_production OWNER trade_dx_user;

-- 権限を付与
GRANT ALL PRIVILEGES ON DATABASE trade_dx_production TO trade_dx_user;

-- 終了
\q
```

### 4. Nginx のインストール（オプション、リバースプロキシ用）

```bash
# Nginxをインストール
sudo apt install nginx -y

# Nginxを起動
sudo systemctl start nginx
sudo systemctl enable nginx

# 状態確認
sudo systemctl status nginx
```

### 5. Git のインストール

```bash
# Gitをインストール
sudo apt install git -y

# 確認
git --version
```

---

## 🔒 セキュリティ設定

### 1. SSH鍵認証の設定（パスワード認証より安全）

#### ローカルPCでSSH鍵を生成（まだの場合）

```bash
# SSH鍵を生成
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 公開鍵をサーバーにコピー
ssh-copy-id root@サーバーIPアドレス
# または
ssh-copy-id ubuntu@サーバーIPアドレス
```

#### サーバー側でパスワード認証を無効化（推奨）

```bash
# SSH設定ファイルを編集
sudo nano /etc/ssh/sshd_config

# 以下の設定を変更
PasswordAuthentication no
PubkeyAuthentication yes

# SSHサービスを再起動
sudo systemctl restart sshd
```

### 2. 自動セキュリティアップデートの設定

```bash
# unattended-upgradesをインストール
sudo apt install unattended-upgrades -y

# 設定を有効化
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. fail2banのインストール（ブルートフォース攻撃対策）

```bash
# fail2banをインストール
sudo apt install fail2ban -y

# fail2banを起動
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# 状態確認
sudo systemctl status fail2ban
```

---

## ✅ セットアップ確認チェックリスト

サーバーセットアップが完了したら、以下を確認してください：

- [ ] SSH接続が正常にできる
- [ ] システムアップデートが完了している
- [ ] タイムゾーンが日本時間（Asia/Tokyo）に設定されている
- [ ] ファイアウォールが適切に設定されている
- [ ] Python 3.11+ がインストールされている
- [ ] Node.js 18+ がインストールされている
- [ ] Gitがインストールされている
- [ ] PostgreSQLがインストールされている（使用する場合）
- [ ] Nginxがインストールされている（使用する場合）
- [ ] SSH鍵認証が設定されている（推奨）

---

## 📝 次のステップ

サーバーセットアップが完了したら、次に進みます：

1. **アプリケーションのデプロイ**
   - Gitリポジトリからコードをクローン
   - 依存関係のインストール
   - 環境変数の設定

2. **データベースの初期化**
   - マイグレーションの実行
   - シードデータの投入

3. **サービス起動設定**
   - systemdでのサービス化
   - 自動起動の設定

4. **リバースプロキシ設定**
   - Nginx設定（オプション）

詳細は [本番運用開始ガイド](./本番運用開始ガイド.md) を参照してください。

---

## 🆘 トラブルシューティング

### SSH接続できない

**原因**: ファイアウォールでSSHポートが閉じている
**解決策**:
```bash
# サーバー側で確認
sudo ufw status
sudo ufw allow 22/tcp
```

### パッケージインストールが失敗する

**原因**: パッケージリストが古い
**解決策**:
```bash
sudo apt update
sudo apt upgrade -y
```

### メモリ不足エラー

**原因**: サーバーリソース不足
**解決策**:
- スワップファイルを作成
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

**最終更新**: 2025-12-15
**バージョン**: V2.1 Web
