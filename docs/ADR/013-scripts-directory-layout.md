# ADR 013: scriptsの機能別ディレクトリ分離

## 状態

採用

## 背景

`scripts/`直下にフォーマッター、Sprite Editor、アニメーションGIF分割など異なる責務のファイルを置くと、作業規則と依存関係の範囲が不明確になる。SFF編集とアニメーションGIF分割は画像を扱うが、入出力形式と処理目的が異なるため、独立した作業単位として管理する必要がある。

## 決定

スクリプトを機能別に分離する。

```text
scripts/
├── formatter/
│   ├── AGENTS.md
│   ├── formatter.py
│   └── test_*.py
├── sprite-editor/
└── animation-gif-spritter/
```

既存の`scripts/AGENTS.md`は`scripts/formatter/AGENTS.md`へ移動し、フォーマッターとその静的検査に適用する。Sprite Editorの実装は`scripts/sprite-editor/`へ追加し、フォーマッターの規約やテストと混在させない。
アニメーションGIF分割の実装は`scripts/animation-gif-spritter/`へ追加し、SFF編集の実装やフォーマッターの規約と混在させない。GIFのフレーム遅延はこの素材分割処理では管理せず、`animation.air`作成時に定義する。

## 結果

フォーマッター、Sprite Editor、アニメーションGIF分割の実装範囲と依存関係を独立して管理できる。ルートのMakefileと各`docs/scripts/`文書は、それぞれのパスを正規の実行先として参照する。
