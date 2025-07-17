﻿# WH_chat_app

## アプリを本番用に変える準備
### ①　必要なパーツをインストールする
```
pip install psycopg2-binary dj-database-url gunicorn
```

|パッケージ名|なにをする？|
|---|---|
|psycopg2-binary|PostgreSQLと接続する道具|
|dj-database-url|環境変数からデータベース情報を読み取る道具|
|gunicorn|サーバーでアプリを動かす本番用のエンジン|

### ②　requirements.txt に記録する
さっきインストールしたものを保存
```
pip freeze > requirements.txt
```
これでRenderが「何をインストールすればいいか」がわかるようになる

---
## データベースの設定を変更
Djangoの設定ファイル settings.py を開いて、次のように変更
### ① もともとのSQLiteの設定をコメントアウト

```
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / "db.sqlite3",
#     }
# }
```

### ② PostgreSQL用の設定を追加
```
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',  # ローカルでは今まで通りSQLite
        conn_max_age=600,
        conn_health_checks=True,
    )
}

```
これは「本番ではPostgreSQLを使うけど、ローカルではまだSQLiteでOKだよ」という設定

---
## サーバでアプリを動かすためのファイルを追加
プロジェクトのルートに Procfile という名前のファイルを作って、以下を記述
```
makefile
コピーする編集する
web: gunicorn your_project_name.wsgi
```
※ your_project_name は settings.py があるフォルダ名に書き換える

---
## GitHubにアプリをアップする
アプリのファイルをGitHubに上げる準備
```
bash
コピーする編集する
git init
git add .
git commit -m "最初のアップロード"
git remote add origin https://github.com/自分のユーザー名/リポジトリ名.git
git push -u origin main
```
⚠️GitHubにまだリポジトリを作ってない人は GitHub にログインして「New」から作ってね！

---
## Renderでアプリを公開！
① Renderにログイン

② 「New」 → 「Web Service」
- GitHubと連携
- あなたのリポジトリを選ぶ
  
③ 設定項目

|項目|入力例|
|---|---|
|Name|my-django-app（好きな名前）|
|Runtime|Python|
|Build Command|pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata data.json|
|Start Command|gunicorn chat_app.wsgi|

---
## PostgreSQLデータベースを作る
1. Renderの左メニューで「Databases」→「New PostgreSQL」
2. 好きな名前で作成（例：`my-db`）
3. 自動的に `DATABASE_URL` という環境変数が作られます
    - Djangoはこれを使ってPostgreSQLに接続します
    - key:DATABASE_URL
    - value:Internal Database URL
      
---
## 管理画面ユーザーを作る
管理画面（admin）を使いたいときは以下を実行
```
python manage.py createsuperuser
```
Render上で実行するか、ローカルで作ってデータを入れ直す

---
## デプロイ前に・・・

settings.py に追加または変更
```
DEBUG = False

ALLOWED_HOSTS = ["*"]
```

## 静的ファイルをまとめる（任意）
CSSや画像をまとめて表示するには whitenoise という道具を使う
```
pip install whitenoise
```
settings.py に追加：
```
import os
MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # 他のミドルウェアたち
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```
staticを集める：
```
python manage.py collectstatic
```
```
pip freeze > requirements.txt
```
を忘れないように注意！！

---
## 完成！
Render がアプリを自動でビルドしてくれたら、URLが表示されます！\
✅ そのURLにアクセスすれば、あなたのDjangoアプリがインターネット上で公開されていることが確認できる！

---
## おまけ：データを移したいとき
今までの SQLite のデータを PostgreSQL に移したいときは以下のようにする
```
python manage.py dumpdata > data.json   # SQLiteのデータを出力
# PostgreSQLに切り替えたあと
python manage.py loaddata data.json     # データを読み込み
```
