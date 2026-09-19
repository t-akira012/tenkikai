# フォーマッター

## 概要

`scripts/formatter/formatter.py` は、TENKIKAIの定義ファイルへ[コーディング規約](../coding-rules.md)を適用するフォーマッターである。

Pythonの標準ライブラリだけを使用する。実行環境と依存関係の管理にはuvを使用し、pipは使用しない。

## 実行方法

リポジトリ直下で次を実行する。

```console
make fmt
```

Makefileから次のコマンドが実行される。

```console
uv run python -B scripts/formatter/formatter.py
```

処理中は対象ファイルと、変更の有無、検証結果、変更ファイル数を端末へ表示する。

## 整形内容

フォーマッターは次の処理を行う。

- テキストファイルの改行コードをLFに統一する。
- 定義ファイルから通常の行コメントと行末コメントを削除する。`;;`で始まる機能塊コメントは保持し、最終検証でも許可する。
- 罫線コメントを、`;` 1文字と `-` 49文字からなる50文字の行へ統一する。
- Statedef見出しを `[statedef NUM]` に統一する。
- State見出しを `[state ]` に統一する。
- StatedefとState内のインデントおよび `=` 前後の空白を削除する。
- StatedefとState内の演算子前後にあるASCII半角スペースを削除する。
- StatedefとState内の `type=` の値をすべて小文字にする。
- StatedefブロックとStateブロックの間へ空行を1行置く。
- `cns/constants.cns` 全体から、引用符内を除くASCII半角スペースを除去する。
- `cns/command.cmd` のコマンド定義から、引用符内を除くASCII半角スペースを除去する。
- `tenkikai.def` の `[Info]` セクションから、引用符内を除くASCII半角スペースを除去する。
- `cns/common1.cns` にも他のCNSファイルと同じ整形規則を適用する。
- `command`をTriggerに使用できる場所を、`cns/command.cmd`のStateDef `-1`内にある入力ビット変換用`VarSet`に限定する。それ以外の場所にある`command` Triggerを検出した場合は、ファイルを書き換える前にエラーで終了する。
- `docs/state/*.md` のステート記述は、挙動をH2見出し、各StateDefの機能をH3見出し `StateDef NUM: 機能名` とする。挙動とStateDefが1対1の場合もこの階層を省略しない。

引用符内の文字列は、コメント削除とASCII半角スペース削除の対象外とする。フォーマッターはStateDefの削除、ファイル間移動、DEF参照先の変更を行わない。

## 検査

ファイルを書き換えず、整形の必要性だけを検査する場合は次を実行する。

```console
make fmt-check
```

`fmt-check`はファイルを変更しない。要整形ファイル、規約外のTrigger配置、StateDef配置などを検出した場合は失敗する。

## common1.cnsの独自管理

WinMUGEN同梱の `common1.cns` に代えて、キャラクターディレクトリ内の `cns/common1.cns` を使用する。

```ini
stcommon=cns/common1.cns
```

これにより、共通ステートもこのリポジトリで管理し、同じフォーマッターを適用できる。

## Common Stateの上書き

StateDef番号が重複する場合の優先順位は、次のとおりとする。

```text
他のステートファイル > cns/common1.cns
```

`cns/command.cmd`、`cns/state.cns`、`cns/observ.cns`、`cns/helper.cns` のいずれかに同じ番号がある場合、WinMUGENはキャラクター固有StateDefを使用する。フォーマッターは`cns/common1.cns`側のStateDefを削除しない。

共通ステートの挙動は、`docs/state/stcommon.md` に記載する。

## テスト

フォーマッターの単体テストと、固定された文書規約の検査は、次のコマンドで実行する。

```console
make test-fmt
```

テストもuv経由で実行し、pipは使用しない。Pythonには `-B` を指定し、`__pycache__` と `.pyc` を生成しない。
