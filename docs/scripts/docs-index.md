# docs-index仕様

## 目的

`docs/`直下の各ディレクトリにあるMarkdown文書を一覧化し、各ディレクトリの`README.md`へ目次を生成する。READMEへ文書の責務や作業規則を手書きせず、それらは同じディレクトリの`AGENTS.md`で管理する。

## 対象

対象は`docs/*/`に直接配置された拡張子`.md`のファイルとする。サブディレクトリは再帰的に探索しない。目次自身である`README.md`と、エージェント向け作業規則である`AGENTS.md`は一覧から除外する。

文書はファイル名で並べ替える。リンクの表示名には各文書の最初のH1見出しを使用し、H1見出しがない場合は拡張子を除いたファイル名を使用する。

## 出力

各`docs/*/README.md`はスクリプトの生成物とし、手書きの本文を保持しない。既存READMEの最初のH1見出しは維持し、READMEが存在しない場合はディレクトリ名から見出しを生成する。

生成内容はH1見出しとMarkdownリンクの箇条書きだけとする。対象文書がないディレクトリもREADMEを生成し、H1見出しだけを記録する。

## 実行方法

リポジトリ直下で次を実行する。

```console
uv run python -B scripts/docs-index/docs_index.py
```

目次生成は次のコマンドで実行する。

```console
make makedocs
```

READMEを書き換えず、更新の必要性だけを確認する場合は次を実行する。

```console
make makedocs-check
```

フォーマッター、フォーマッター検査、目次生成をまとめて実行する場合は、次のコマンドを使用する。

```console
make run
```

`make run`は`make fmt`、`make test-fmt`、`make makedocs`の順に実行する。処理中は対象ディレクトリ、READMEの更新有無、完了件数を端末へ表示する。

`make check`は`make fmt-check`、`make test-fmt`、`make makedocs-check`の順に実行し、ファイルを変更しない。pre-commitでは`make check`を使用する。

## 責務外

- 文書本文の要約や説明文の生成
- `docs/`直下のMarkdown文書の一覧化
- `AGENTS.md`の生成または変更
- Markdown文書の内容や書式の修正
- サブディレクトリを含む再帰的な目次生成
