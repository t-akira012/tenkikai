# フォーマッター

## 概要

`scripts/formatter.py` は、TENKIKAIの定義ファイルへ[コーディング規約](coding-rules.md)を適用するフォーマッターである。

Pythonの標準ライブラリだけを使用する。実行環境と依存関係の管理にはuvを使用し、pipは使用しない。

## 実行方法

リポジトリ直下で次を実行する。

```console
make fmt
```

Makefileから次のコマンドが実行される。

```console
uv run python -B scripts/formatter.py
```

処理中は対象ファイルと、変更の有無、検証結果、変更ファイル数を端末へ表示する。

## 整形内容

フォーマッターは次の処理を行う。

- テキストファイルの改行コードをLFに統一する。
- 定義ファイルから通常の行コメントと行末コメントを削除する。
- 罫線コメントを、`;` 1文字と `-` 49文字からなる50文字の行へ統一する。
- Statedef見出しを `[statedef NUM]` に統一する。
- State見出しを `[state ]` に統一する。
- StatedefとState内のインデントおよび `=` 前後の空白を削除する。
- StatedefとState内の演算子前後にあるASCII半角スペースを削除する。
- StatedefとState内の `type=` の値をすべて小文字にする。
- StatedefブロックとStateブロックの間へ空行を1行置く。
- `cns/constants.cns` 全体からASCII半角スペースを除去する。
- `cns/command.cmd` のコマンド定義からASCII半角スペースを除去する。
- `tenkikai.def` の `[Info]` セクションからASCII半角スペースを除去する。
- `tenkikai.def` の分割ファイル参照を正規化する。
- `cns/common1.cns` にも他のCNSファイルと同じ整形規則を適用する。
- `cns/common1.cns` と他のステートファイルで重複するStateDefを、`cns/common1.cns` 側から削除する。

整形前後の有効な定義を内部で比較し、コメントと書式以外の内容が変化した場合はエラーで終了する。

## 旧t.cnsの分割

旧構成の `t.cns` が存在する場合は、StateDef番号に従って次のファイルへ分割する。

| 出力先 | 内容 |
| --- | --- |
| `cns/constants.cns` | キャラクター定数 |
| `cns/state.cns` | 0以上9999以下のStateDef |
| `cns/observ.cns` | StateDef `-2`と`-3` |
| `cns/helper.cns` | 10000以上のStateDef |

分割後、旧 `t.cns` は削除し、`cns/` 配下へ出力して `tenkikai.def` の参照を更新する。

## common1.cnsの独自管理

WinMUGEN同梱の `common1.cns` に代えて、キャラクターディレクトリ内の `cns/common1.cns` を使用する。

```ini
stcommon=cns/common1.cns
```

これにより、共通ステートもこのリポジトリで管理し、同じフォーマッターを適用できる。

## StateDefの優先順位

StateDef番号が重複する場合の優先順位は、次のとおりとする。

```text
他のステートファイル > cns/common1.cns
```

`cns/command.cmd`、`cns/state.cns`、`cns/observ.cns`、`cns/helper.cns` のいずれかに同じ番号がある場合、フォーマッターは `cns/common1.cns` 側のStateDefブロックを削除する。

共通ステートの挙動は、`docs/state/state-stcommon.md` に記載する。

## テスト

フォーマッターの単体テストと、StateDef文書および生成物一覧と実装の対応検査は、次のコマンドで実行する。

```console
make test-fmt
```

テストもuv経由で実行し、pipは使用しない。Pythonには `-B` を指定し、`__pycache__` と `.pyc` を生成しない。
