# Qiita記事を推薦してくれる日報アプリ
研修の一環 + 個人的な興味でJubatusを使ってみよう！
という趣旨で、Qiita記事を推薦してくれる機能を（知り合いが作った）日報アプリに（勝手に）実装してみました。
ユーザが日報を投稿すると、Jubatus＋Mecabが日報内容を解析し、類似したQiitaの記事をおすすめしてくれるような機能です。
Jubatus（のRecommender）で何かアプリを作ってみよう、という方に参考になれば幸いです。

知り合いが作った日報アプリ：https://github.com/hayashizakitakaaki/Introduction_mysite

私が主に実装したのは、qiita/以下のみです。

## 目次
* [概要](#概要)
* [特徴と機能](#特徴と機能)
* [使い方](#使い方)
* [開発環境](#開発環境)
* [バージョン情報](#バージョン情報)
* [ライセンス](#ライセンス)

## 概要
メイン処理となるのは、juba_update.pyとjuba_analyze.pyです。

| File                            | explain |
|:--------------------|:------------------------|
| qiita_api                       |  |
|   ｜＿ auth_info.json.dummy     | QiitaAPIの認証情報を記載 |
|   ｜＿ qiita2.py                | QiitaAPIWrapperを参考にさせて頂いています http://qiita.com/tag1216/items/7e23630d97293e35ea4c#_reference-6a490306bbc181488c3c  |
| settings.json                   |  Recommenderサーバの設定ファイル |
| juba_abstract.py                | Recommenderサーバに接続するための情報をまとめたクラス |
| __juba_analyze.py__             | 日報本文から、類似するQiita記事を推薦する機能 |
| __juba_update.py__              | 事前に収集したQiita記事のjsonファイルを読み込み、日報本文に出現する名詞とその出現回数を特徴量として、サーバにアップロードする。 |
| juba_save.py                    | 学習モデルを外部ファイルにエクスポートする機能 |
| mecab.py                        | 日報本文から名詞のみを抽出する特長抽出器 |
| services.py                     | 共通して使用するメソッド群 |
|  views.py                       | DjangoからQiita推薦機能を呼び出すときの処理 |

view.pyで記述したメソッドを、Intoroduction_mysite/dailyreport/views.pyのview_daily_detail関数内107行目あたりで呼ぶことで、推薦機能をDjangoから呼び出しています。

## 開発環境

環境は以下の通りです。
* CentOS 7
* Python 3.5.2
* jubatus 0.9.1
* mecab-python3 0.7


### 初期設定
### 実行方法

　アプリケーションを実行するには以下のコマンドをコマンドラインから入力してください。
~~~
> python manage.py runserver
~~~
　実行後、以下のアドレス(初期設定の場合)をWebブラウザに入力し、アプリケーションのログイン画面にアクセスします。
~~~
http://127.0.0.1:8000/login/
~~~
　[初期設定](#djangoモデルの初期設定)の際に登録した管理ユーザーでもログインすることができます。また、ユーザー登録、およびその後の使い方については、[使い方](#使い方)を参照してください。

## バージョン情報

## 謝辞
日報アプリを使わせて頂いたhayashizakitakaaki氏に多大なる感謝を。


## ライセンス

Copyright (c) 2016 Takaaki Hayashizaki

This software is released under the MIT License, see LICENSE.
