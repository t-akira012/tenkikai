# AGENTS.md

このリポジトリは、WinMUGEN用キャラクター「TENKIKAI」のキャラクターディレクトリです。

Codexの動作環境はmacOS上である。WinMUGENはWindows 11 on VMware上で動作するため、挙動の実機検証はユーザーに任せる。Codexによる技や移動などの動作検証は、定義、遷移条件、座標、速度、時間、ダメージなどに基づいて数学的に行うこと。

`docs/state/*.md` の動作定義とCNSファイルのステート定義に差異がある場合は、ユーザーへ報告すること。どちらをマスターとするかは定義されていない。Codexは差異のある記述とCNS定義をユーザーへ提示し、どちらを正として修正するかは場合ごとのユーザー指示に従うこと。

仮想環境や共有フォルダーとの同期後に検出した未コミット差分は、共有更新によるものと推測せず、ユーザーによる手動修正として扱う。ユーザー修正はCodexの修正より優先し、内容を上書き、削除、リバートしてはならない。差分が作業対象と衝突する場合は、ユーザー修正を保持したまま影響を報告し、明示的な指示を受けること。

作業時は、次の文書に従ってください。

- [コーディング規約](docs/coding-rules.md)
- [フォーマッター](docs/scripts/formatter.md)
- [キャラクターデザイン](docs/DESIGN.md)
- [設計文書の記述規則](docs/design/AGENTS.md)
- [ステートドキュメント](docs/state/README.md)
- [ステート文書の作業規則](docs/state/AGENTS.md)
- [StateDef -1/-2/-3 の作業規則](docs/AGENTS.state-controller.md)
- [Helperルーティング規約](docs/AGENTS.helper.md)
- [Trigger記述規則](docs/AGENTS.trigger.md)
- [コマンド入力・行動設計規約](docs/AGENTS.command.md)
- [入力ビットマップ](docs/AGENTS.input-map.md)
- [オートメーション規約](docs/AGENTS.automation.md)
- [設計判断記録](docs/ADR/)
- [バグ修正](docs/issues/)
- [公式ドキュメント未記載のユーザー調査情報](docs/researched/README.md)
- [スクリプト作業規則](scripts/formatter/AGENTS.md)
- [スクリプト共通作業規則](scripts/AGENTS.md)

## `docs/`の文書体系

`docs/`配下の文書は、役割、固定性、コードとの関係に応じて配置する。新しい文書は、名称や一時的な作業場所ではなく、次の定義に従って配置先を決める。

### `docs/DESIGN.md`

`docs/DESIGN.md`は、TENKIKAIのキャラクター全体に関する上位設計およびキャラクターデザインである。キャラクター像、動きの方向性、攻撃体系、浮遊感、採用または不採用とする表現などを定め、作品に関する美的判断の源泉とする。

CNSの都合、一般的な実装慣習、構造化の都合だけで、`docs/DESIGN.md`の美的方針を変更してはならない。詳細設計、ステート文書、実装案は、原則としてこの文書が示す表現意図を満たす方向で検討する。ただし、上位設計に記載されていない具体的な挙動や数値を推測によって確定してはならず、表現上の判断が必要な場合はユーザーへ確認する。

### `docs/design/`

`docs/design/`は、`docs/DESIGN.md`を具体化する動作モデル、状態・処理関係、表現設計、現在の設定値を扱う。設計文書にはユーザーが確定した要求を記載し、実機確認中の試験値や未確定の表現を確定事項として記録しない。詳細な記述方法は`docs/design/AGENTS.md`に従う。

### `docs/state/`

`docs/state/`は、現在のCNSおよびCMD実装から読み取った動作、StateDef、Controller、Trigger、変数、Helper、Explod、Projectileなどを記録する、流動的な文書群である。コード変更に伴って更新されるが、コードから機械的に生成されるだけの従属文書ではない。

ステート文書とコードのどちらが常に正しいかは定めない。差異を検出した場合は、文書をコードへ機械的に合わせたり、コードを文書へ機械的に戻したりしてはならない。差異のある記述と実装を具体的に提示し、変更経緯、確定済み要件、上位設計、ユーザーの意図および指示に基づいて、文書またはコードを流動的に適応させる。

`docs/state/README.md`は文書一覧の生成物とし、作業規則は`docs/state/AGENTS.md`に定める。個別の動作文書や一覧を更新する場合は、`docs/state/AGENTS.md`の規則に従う。

### その他の文書群

| 配置 | 定義 |
| --- | --- |
| `docs/AGENTS.*.md` | エージェントが従う固定的な作業規則および実装契約。ユーザーの明示的な承認なしに、確定済みの方針や割り当てを変更しない。 |
| `docs/automation/` | オートメーション中の行動ごとに、距離、位置、State、時間などを用いる具体的な自動判断を記録する。共通の有効化・入力切替規約は`docs/AGENTS.automation.md`に置く。 |
| `docs/ADR/` | 採用した設計判断の背景、決定、結果を残す履歴。現在の実装一覧ではなく、判断の理由を記録する。 |
| `docs/issues/` | 不具合の症状、原因、修正内容、確認事項を記録する。 |
| `docs/researched/` | 公式文書に記載されていない、ユーザーが調査したWinMUGENの仕様を記録する。 |
| `docs/scripts/` | `scripts/`に配置する補助ツールの目的、入出力、運用方法、作業手順を記録する。ツールの実装規則は各スクリプトディレクトリの`AGENTS.md`に従う。 |
| `docs/`直下のその他の文書 | コーディング規約、フォーマッター、リポジトリ全体へ適用する運用文書を配置する。 |

- 注意: AGENTS.md の 子 AGENTS.*.md は、`docs/AGENTS.*.md` に配置する。

## WinMUGEN コーディングについて

WinMUGEN は LLM 学習データが不足している。一方で、ユーザーはWinMUGENの仕様に詳しい。

仕様の不明点は、共通規約、および、ユーザー調査情報を読み解き、必要に応じて、ユーザーに詳細仕様を質問すること。

### 一般のプログラミングパラダイムを不採用とする

WinMUGENでは、一般的なプログラミングパラダイムの関心の分離や疎結合化を常に優先しない。

Helper、StateDef、Redirect、Var/FVar、State Controllerはゲーム内部の実行順と仕様に結びついているため、RootとHelperの直接監視・更新や、複数の役割を一体化した実装が適切な場合がある。

構造化や疎結合化は手段として扱い、ゲーム仕様、実行順、State奪取、常時監視、Helper・変数制限、演出同期を満たす実装を優先すること。

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
