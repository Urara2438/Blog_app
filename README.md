⚪️ タイトル：日記Webアプリ
  Python，FlaskおよびPostgreSQLを使用して作成したシンプルな日記投稿アプリです．
  ログイン機能を実装しており，管理者のみが日記の作成・編集・削除を行えるようになっています．
  また，画像アップロード機能にも対応しています．

⚪️ 操作画面
  トップページ：日記のタイトル一覧を表示
  ログイン画面：ログイン
  サインアップ画面：サインアップ
  管理者ページ：日記の新規作成，編集，削除
  日記詳細ページ：本文と画像の表示

⚪️ 使用技術

  Python
  Flask
  Flask-SQLAlchemy
  Flask-Migrate（Alembic）
  PostgreSQL
  HTML

⚪️ データベース設計
  usersテーブル
  カラム名	型	説明
  id	integer	主キー
  user_name	varchar(50)	ユーザー名
  password	varchar(500)	ハッシュ化されたパスワード
  
  article テーブル
  カラム名	型	説明
  id	integer	主キー
  title	varchar(50)	タイトル
  body	varchar(5000)	本文
  created_at	timestamp	作成日時
  img_name	varchar(100)	画像ファイル名

⚪️ 環境構築
① リポジトリをクローン
git clone https://github.com/yourname/flask-diary-app.git
cd flask-diary-app

② 仮想環境の作成（任意）
python -m venv venv
source venv/bin/activate  # Mac
venv\Scripts\activate     # Windows

③ ライブラリのインストール
pip install -r requirements.txt

🗄 PostgreSQL 設定
CREATE DATABASE diary_app;


Flask 側の設定例：

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://postgres:password@localhost/diary_app"

▶️ 起動方法
flask run


または

python app.py


アクセス：

http://127.0.0.1:5000

💡 工夫した点

CRUD（作成・表示・編集・削除）を一通り実装

ログイン機能を導入し、管理者のみ操作可能にした

画像アップロード機能を実装

Flask-Migrate によるマイグレーション管理

DB設計 → 画面設計 → 実装の一連の流れを自力で構築

😇 苦労した点・学んだこと

Flask と PostgreSQL の接続設定で何度もエラーにハマった

SQLAlchemy のマイグレーション管理の仕組みを理解するのに時間がかかった

ログイン状態の管理（セッション管理）の考え方を理解できた

Webアプリ開発の「全体の流れ」を掴めたのが一番の収穫

🚀 今後の改善予定

ページネーション対応

検索機能

デザイン改善（Bootstrap / Tailwind導入）

ユーザーごとに投稿を管理

本番環境へのデプロイ（Render / Fly.io など）

🧑‍💻 作者

作成者: Kentaro Yoneda

学習目的で作成したポートフォリオ作品です。
