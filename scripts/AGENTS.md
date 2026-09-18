# scripts共通作業規則

## Python実行環境

scripts配下のPythonツールと検査は、uvで実行する。pip、`pip install`、システムPythonへの直接インストールは使用してはならない。

依存関係を追加する場合は、`pyproject.toml`またはuvの管理対象へ明示し、`uv run`から再現可能な状態にする。実行例は次の形式とする。

```console
uv run python -B scripts/formatter/formatter.py
uv run python -B scripts/sprite-editor/sprite_editor.py --help
```

フォーマッター固有の規則とテスト責務は[formatter/AGENTS.md](formatter/AGENTS.md)に従う。Sprite Editor固有の規則は[sprite-editor/](sprite-editor/)へ追加する。
