Flask のアプリを起動する方法は下記の通りです。Windows の方は「python」だけで結構です。

```bat
python3 run.py
```

起動したら、下記のアドレスにアクセスして下さい。

http://127.0.0.1:5200

Flask の日本語のリファレンスは以下のとおりです。
https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/

## 2023.04.19 以前にこのレポジトリを Fork / Clone した方へ

タグを全部消してブランチ名を全て変更したので、一旦レポジトリを削除して頂き、再度 Fork / Clone してください。
大変申し訳ございません。

## 講義の内容とブランチについて

講義の内容に応じてソースコードの差分を確認したい場合、以下のブランチをチェックアウトしてください。
`master` ブランチに全ての成果物が入っています。

| 回                                     | ブランチ       |
| -------------------------------------- | -------------- |
| 第 1 回 - Web アプリの基礎 -           | 01_flask_basic |
| 第 2 回 - ユーザー登録(サインアップ) - | 02_signup      |
| 第 3 回 - ログイン -                   | 03_login       |
| 第 4 回 - 記事の作成と表示 -           | 04_add_post    |
| 第 5 回 - 記事の編集と削除、総まとめ - | master         |

### 改訂履歴

#### 2020.06.10

- ライブラリを最新化しました。

#### 2021.04.07

- ライブラリを最新化しました。
- Python3.9.2 で動作確認を取っています。

#### 2023.04.19

- ライブラリを最新化し、Python3.11.3 で動作確認を取りました。
- タグを全部消して、ブランチに切り替えました。
- SQLAlchemy が 2.0 系になりましたが、マイグレーションコストが高いので、SQLAlchemy1 系の最新版、1.4.47 固定にしました。
- `SQLALCHEMY_DATABASE_URI` で相対パスを指定すると、 `instance` フォルダ配下の相対パスに変わったため、DB ファイルへの参照を絶対パスに変更しました。
- Mac の場合`AirDrop`が`5000`ポートを使うことがあるので、`5200`に変更しました。
