# Project

記事を投稿したり、気になる人の記事を見たりコメントできる
アプリケーションです。

# 実装した機能

- ユーザー情報

  - アカウント作成
  - ログイン・ログアウト
  - ユーザ検索

- プロフィール

  - プロフィール編集（プロフィール画像、背景画像、名前、自己紹介）
  - フォロー、フォロワーの一覧表示
  - 投稿した記事を表示
  - 投稿したメディアを表示
  - いいねをした記事を表示
  - フォロー、フォローの解除

- 記事

  - 記事投稿
  - フォローした人の記事を表示
  - 記事に対してコメントする
  - コメント数を表示
  - 記事に対していいねする
  - いいね数表示を表示
  - 記事にいいねしたユーザを表示

- ユーザ同士１対１のメッセージ（メッセージ送信、受信の自動更新）

# 技術

## 言語

- フロント

  - HTML/CSS
  - JavaScript
  - jQuery
  - Bootstrap4
  - AdminLTE3

- バックエンド
  - Python3
  - Django2.2.4
  - Django REST Framework3.9.0

## インフラ

- インフラ構成図

  ![Infrascracture](https://user-images.githubusercontent.com/53550752/88672688-b391ee00-d122-11ea-9123-4a883efef3dd.jpg)

- AWS

  - ALB / EC2 / VPC / RDS(PostgreSQL) / S3 / Route53 / ACM / ElasticCache

- Docker

  - Docker
  - docker-compose

- Nginx

- Gunicorn

# ER 図

![Article-ER](https://user-images.githubusercontent.com/53550752/88674055-4b440c00-d124-11ea-8819-379e9172062b.jpg)
