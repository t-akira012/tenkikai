# AGENTS.md

このリポジトリは、WinMUGEN用キャラクター「TENKIKAI」のキャラクターディレクトリです。

Codexの動作環境はmacOS上である。WinMUGENはWindows 11 on VMware上で動作するため、挙動の実機検証はユーザーに任せる。Codexによる技や移動などの動作検証は、定義、遷移条件、座標、速度、時間、ダメージなどに基づいて数学的に行うこと。

`docs/state/*.md` の動作定義とCNSファイルのステート定義に差異がある場合は、ユーザーへ報告すること。どちらをマスターとするかは定義されていない。Codexは差異のある記述とCNS定義をユーザーへ提示し、どちらを正として修正するかは場合ごとのユーザー指示に従うこと。

作業時は、次の文書に従ってください。

- [コーディング規約](docs/coding-rules.md)
- [フォーマッター](docs/formatter.md)
- [キャラクターデザイン](docs/DESIGN.md)
- [ステートドキュメント](docs/state/README.md)
- [ステート文書の作業規則](docs/state/AGENTS.md)
- [StateDef -1/-2/-3 の作業規則](docs/AGENTS.state-controller.md)
- [Trigger記述規則](AGENTS.trigger.md)
- [設計判断記録](docs/ADR/)
- [公式ドキュメント未記載のユーザー調査情報](docs/researched/README.md)

## 共通規約の参照

M.U.G.E.N コーディングに関する共通規約は、このファイルへ転載せず、次の外部文書を参照すること。
トークンを節約するため、共通規約のウェブ文書は参照せず、ローカル文書を厳守すること。

- GitHub文書: <https://github.com/t-akira012/mugen-docs-coding-agents>
- 共通Agent規約（日本語）: `~/src/github.com/t-akira012/mugen-docs-coding-agents/AGENTS.ja.md`
- CNS中核仕様: `~/src/github.com/t-akira012/mugen-docs-coding-agents/docs/CNS_CORE.md`
- 互換性方針: `~/src/github.com/t-akira012/mugen-docs-coding-agents/docs/COMPATIBILITY.md`

## `do-not-read-coding-agent.md`

ユーザー作業用ファイルであり、Coding AgentsはRead/Write禁止
