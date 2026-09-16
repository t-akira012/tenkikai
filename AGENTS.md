# AGENTS.md

このリポジトリは、WinMUGEN用キャラクター「TENKIKAI」のキャラクターディレクトリです。

Codexの動作環境はmacOS上である。WinMUGENはWindows 11 on VMware上で動作するため、挙動の実機検証はユーザーに任せる。Codexによる技や移動などの動作検証は、定義、遷移条件、座標、速度、時間、ダメージなどに基づいて数学的に行うこと。

`docs/state/*.md` の動作定義とCNSファイルのステート定義に差異がある場合は、ユーザーへ報告すること。どちらをマスターとするかは定義されていない。Codexは差異のある記述とCNS定義をユーザーへ提示し、どちらを正として修正するかは場合ごとのユーザー指示に従うこと。

仮想環境や共有フォルダーとの同期後に検出した未コミット差分は、共有更新によるものと推測せず、ユーザーによる手動修正として扱う。ユーザー修正はCodexの修正より優先し、内容を上書き、削除、リバートしてはならない。差分が作業対象と衝突する場合は、ユーザー修正を保持したまま影響を報告し、明示的な指示を受けること。

作業時は、次の文書に従ってください。

- [コーディング規約](docs/coding-rules.md)
- [フォーマッター](docs/formatter.md)
- [キャラクターデザイン](docs/DESIGN.md)
- [設計文書の記述規則](docs/design/AGENTS.md)
- [ステートドキュメント](docs/state/README.md)
- [ステート文書の作業規則](docs/state/AGENTS.md)
- [StateDef -1/-2/-3 の作業規則](docs/AGENTS.state-controller.md)
- [Trigger記述規則](docs/AGENTS.trigger.md)
- [設計判断記録](docs/ADR/)
- [バグ修正](docs/issues/)
- [公式ドキュメント未記載のユーザー調査情報](docs/researched/README.md)


- 注意: AGENTS.md の 子 AGENTS.*.md は、`docs/AGENTS.*.md` に配置する。

## WinMUGEN コーディングについて

WinMUGEN は LLM 学習データが不足している。一方で、ユーザーはWinMUGENの仕様に詳しい。

仕様の不明点は、共通規約、および、ユーザー調査情報を読み解き、必要に応じて、ユーザーに詳細仕様を質問すること。

## 演出などの数学的表示について

Explod などの表示軌道を描く演出処理はゲーム開発に利用される数学で解け、LLMの学習が豊富である。

ユーザーの演出要望に従って、どのような数学的処理を適用するかを相談しなさい。

## 共通規約の参照

WinMUGEN コーディングに関する共通規約は、このファイルへ転載せず、次の外部文書を参照すること。
トークンを節約するため、共通規約のウェブ文書は参照せず、ローカル文書を厳守すること。

- GitHub文書: <https://github.com/t-akira012/mugen-docs-coding-agents>
- 共通Agent規約（日本語）: `~/src/github.com/t-akira012/mugen-docs-coding-agents/AGENTS.ja.md`
- CNS中核仕様: `~/src/github.com/t-akira012/mugen-docs-coding-agents/docs/CNS_CORE.md`
- 互換性方針: `~/src/github.com/t-akira012/mugen-docs-coding-agents/docs/COMPATIBILITY.md`

## `do-not-read-coding-agent.md`

ユーザー作業用ファイルであり、Coding AgentsはRead/Write禁止
