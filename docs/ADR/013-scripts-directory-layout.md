# ADR 013: scriptsの機能別ディレクトリ分離

## 状態

採用

## 背景

`scripts/`直下にフォーマッター、フォーマッター検査、Sprite Editorなど異なる責務のファイルを置くと、作業規則と依存関係の範囲が不明確になる。Sprite EditorはSFFと画像を扱うため、定義ファイルを整形するフォーマッターとは独立した作業単位として管理する必要がある。

## 決定

スクリプトを機能別に分離する。

```text
scripts/
├── formatter/
│   ├── AGENTS.md
│   ├── formatter.py
│   └── test_*.py
└── sprite-editor/
```

既存の`scripts/AGENTS.md`は`scripts/formatter/AGENTS.md`へ移動し、フォーマッターとその静的検査に適用する。Sprite Editorの実装は`scripts/sprite-editor/`へ追加し、フォーマッターの規約やテストと混在させない。

## 結果

フォーマッターの実行・テスト対象とSprite Editorの実装範囲を独立して管理できる。ルートのMakefileと`docs/scripts/formatter.md`は、新しいパスを正規の実行先として参照する。
