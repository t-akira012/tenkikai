---
name: create-waza
description: TENKIKAIの技、攻撃、特殊移動、技に伴う演出を自然言語から設計し、新規作成または変更する。未確定事項のユーザー確認、明示承認された試験用の版付きKFM候補、WinMUGENのCNS、CMD、AIR、Helper、Explod、Projectile、入力、オートメーション、the_controller連携を扱う技作業で使用する。
---

# Create Waza

TENKIKAI固有の設計とWinMUGENの実行順を維持する。関連文書は必要なものだけを読む。

## 調査範囲を決める

1. ルートの`AGENTS.md`へ従う。
2. [技仕様文書の作業規則](../../../docs/attacks/AGENTS.md)、[階層スキーマ](../../../docs/attacks/structure.md)、[仕様解決手順](../../../docs/attacks/specification-resolution.md)を読む。
3. 入力、移動、攻撃判定、アニメーション、Helper、全体演出のうち対象要素を特定し、`rg`で関連するStateDef、Action、変数、文書を探す。
4. `docs/DESIGN.md`、`docs/design/`、後述の条件別文書から該当箇所だけを読む。
5. 対象コードと`docs/state/`を照合する。差異は自動解消せず、具体的にユーザーへ提示する。

上位設計にない見た目、時間、速度、ダメージ、無敵、色、軌道を推測で確定しない。美的判断またはゲームバランスの判断が必要な場合は実装前に確認する。

## the_controllerの責務

`the_controller`は、Helper Armorと仮想ライフ、PlayerPush、無敵、Rootアニメーション時間、Body・Head・Auraの変換、Aura Bound、AllPalFX、複数Helper間の演出値を統合管理する。既存責務をRootや新規管理Helperへ複製しない。新しい全体制御を追加する場合は、責務の追加をユーザーへ提示する。

## HeadとHead Auraの実装契約

技によってHeadまたはHead Auraの位置、Offset、AngleDraw、表示、残像を変更する場合は、[ADR 023](../../../docs/ADR/023-head-head-aura-transform-synchronization.md)と[ADR 024](../../../docs/ADR/024-head-head-aura-controller-managed-position-and-visibility.md)に従う。

- 技固有の条件判定とHead系の完成値（Pos、Offset、AngleDraw、表示、残像）は`the_controller`で確定する。HeadとHead AuraへRootのStateNo判定や計算式を複製しない。
- Head AuraはHeadとの同期を標準とする。非同期化する場合だけ、`the_controller`へプロパティ別の非同期フラグと対象別完成値を設け、他のプロパティへ波及させない。
- HeadとHead Auraは割り当てられた完成値を各プロパティにつき一度だけ適用する。後段上書きや表示結果だけを合わせる補正へ依存しない。

現行値と経路は、[the_controller](../../../docs/state/helper-99004-the-controller.md)、[Head](../../../docs/state/helper-99001-the-head.md)、[Head Aura](../../../docs/state/helper-99003-the-head-aura.md)、[変数一覧](../../../docs/state/var-list.md)、[helper.cns](../../../cns/helper.cns)から確認する。

## 固定遷移契約

`the_controller`の挙動塊は増加してよいが、次の遷移方式は変更しない。

```text
集約StateDef 99004000
→ 挙動塊のルーター
→ 該当する個別挙動を0個または1個実行
→ 次の挙動塊のルーター
→ すべての挙動塊を固定順で処理
→ 終端StateDef 99004999
→ StateDef 5150
```

- 各挙動塊にルーターと個別挙動StateDefを分けて置く。
- 個別挙動の成立・不成立の両経路を同じ次のルーターへ接続し、挙動塊を固定順で通過させる。
- 最後の挙動塊だけを終端へ接続する。個別挙動から集約StateDefへ戻さない。
- 挙動塊を追加する場合は順序を確定し、直前と直後の両経路を接続する。

現在のStateDef番号、変数割当、挙動塊一覧は固定コピーせず、[helper.cns](../../../cns/helper.cns)、[the_controllerステート文書](../../../docs/state/helper-99004-the-controller.md)、[変数一覧](../../../docs/state/var-list.md)の該当箇所から確認する。

## 必要な設計判断だけを読む

技が該当する場合に限り、次の文書を読む。

| 必要な処理 | 参照先 |
| --- | --- |
| 新しい挙動塊、ルーティング変更 | [ADR 006](../../../docs/ADR/006-controller-routing.md)、[ADR 015](../../../docs/ADR/015-the-controller-99004-routing.md)、[Helper規約](../../../docs/AGENTS.helper.md) |
| Helper Armor、ライフ、ダメージ | [ライフ管理方式](../../../docs/design/005-life-management.md)、必要に応じて[GetHitVar](../../../docs/researched/gethitvar.md)と[HitOverride](../../../docs/researched/hitoverride.md) |
| PlayerPush、すり抜け | [ADR 017](../../../docs/ADR/017-playerpush-disable-flag.md) |
| 無敵 | [ADR 018](../../../docs/ADR/018-the-controller-invincibility-flag.md) |
| Rootアニメーション時間 | [ADR 019](../../../docs/ADR/019-controller-root-animtime.md)、[Rootアニメーション時間保持規約](../../../docs/AGENTS.root-animtime.md) |
| 通常移動、浮遊移動、ダッシュ、回避、突進、ワープ、技固有移動 | [移動・速度管理規約](../../../docs/AGENTS.movement.md)、[ADR 026](../../../docs/ADR/026-velocity-based-continuous-movement.md) |
| AngleDrawの解除・共有 | [ADR 010](../../../docs/ADR/010-angledraw-reset.md)、[ADR 020](../../../docs/ADR/020-controller-angledraw-sharing.md) |
| HeadとHead Auraの位置、変換、表示、残像 | [ADR 023](../../../docs/ADR/023-head-head-aura-transform-synchronization.md)、[ADR 024](../../../docs/ADR/024-head-head-aura-controller-managed-position-and-visibility.md) |
| Aura Bound | [Aura Bound設計](../../../docs/design/003-aura-bound.md) |
| エフェクトの追加・変更 | [エフェクト作業規則](../../../docs/AGENTS.effect.md)、[エフェクト設計一覧](../../../docs/design/008-effects.md)、対象個別文書。AllPalFXは[ADR 021](../../../docs/ADR/021-controller-allpalfx-routing.md)も読む |

## 技を設計する

ユーザー入力は自然言語で受ける。JSONまたはYAMLへの書き直しを要求しない。技仕様の正本はMarkdownとする。

次の順で仕様を解決する。

1. ユーザー要求を自然言語のまま個別技文書へ記録する。
2. 技分類を決める。この時点で`common-v1`または分類プロファイルを適用しない。
3. [State Controller対応](../../../docs/attacks/state-controller-map.md)を使い、実装責務を割り当てる。
4. 既存の確定事項とユーザー要求だけでは決まらない全項目を列挙し、ユーザーへ質問する。
5. 試験実装が目的の場合に限り、版名、適用項目および具体値を提示して、デフォルト候補を採用してよいか質問できる。
6. 全項目を「ユーザー指定」「対象外」「ユーザー承認済み」のいずれかへ解決する。試験用デフォルト候補は、ユーザーが明示承認した項目だけを「ユーザー承認済み」の試験値として扱う。
7. 演出と攻撃定義の時刻、位置、持続、命中時演出が同期することを確認する。
8. 解決済み仕様をユーザーが承認してから実装する。

未確定事項を、推測、一般的なゲーム慣習、KFM値、`common-v1`または分類プロファイルによって自動的に採用してはならない。ユーザーが回答しないことを承認とみなさず、未確定事項を残したまま仕様確定または実装へ進まない。

分類デフォルトは[デフォルト候補一覧](../../../docs/attacks/defaults/README.md)として扱う。ユーザーへ試験値を提案するために必要な候補だけを読み、承認前に仕様へ適用しない。数値候補は`../kfm/kfm.cns`と`../kfm/kfm.cmd`を根拠とし、KFMに対応実装がないProjectileとReversalDefを推測で補完しない。ユーザーが試験用として明示承認した版名、項目および値だけを個別技文書へ記録し、確定値と区別する。既存技へ新版を自動適用しない。

### Powerは明示指定だけを扱う

Power関連は特に明示的に扱う。ユーザーがPowerの消費、増加、取得、相手への付与または固定を指定しておらず、提示した試験値についても承認していない場合は、次を厳守する。

- 個別技文書へPowerの値または「なし」を補わない
- KFMまたは分類プロファイルのPower値を、一般デフォルト候補の一部として採用または提示しない
- `poweradd`、`getpower`、`givepower`、`PowerAdd`または`PowerSet`を実装しない
- 試験用デフォルトを提案する場合、Powerを他項目へ隠して一括承認の対象にせず、具体値を独立して提示する

既存技を変更する場合、既存のPower処理はユーザー修正として保持する。依頼内容と衝突する場合だけ現行処理を提示して指示を受け、明示指示なしに追加、変更または削除しない。

実装前に次を確定する。既存の確定事項とユーザー指定から求められない項目は、省略せずユーザーへ確認する。

- StateDef、遷移元・遷移先、終了・中断時の復帰先
- 入力ビット、オートメーション判断、Action、素材、表示要素
- StateType、MoveType、Physics、Ctrl、座標、速度、時間、移動式
- HitDef、Helper、Explod、Projectile、ダメージ、無敵、PlayerPush
- `the_controller`へ渡す演出要求と発動時刻

ガード不能、ガードクラッシュ、アーマー・無敵・Projectile防御の貫通、ReversalDef、長時間または完全無敵、相手State奪取、即死級ダメージ、外部キャラクター固有仕様への依存は、実装前にユーザー承認を得る。防御突破は単なる有無ではなく、無視、軽減不適用、消費、破壊、ダメージ通過などの作用を確定する。

新しいエフェクト種別または表現パターンは、CNS実装前に一覧へ登録し、個別設計文書を作成または更新する。

Commandを直接参照できるのはStateDef `-1`の入力ビット変換だけとする。技遷移と技中処理は入力ビットまたは状態情報を使用する。入力を追加する場合だけ`docs/AGENTS.input-map.md`、`docs/AGENTS.command.md`、`docs/AGENTS.automation.md`を読む。

## 実装と確認

1. ユーザーの未コミット変更を保持する。
2. CNS、CMD、AIRと必要な流動文書を同時に更新する。
3. 変数、StateDef、Action、Helper IDの衝突と、遷移・座標・速度・時間・ダメージを検証する。
4. `make check`を実行する。
5. WinMUGEN実機で確認すべき操作、表示、当たり判定をユーザーへ渡す。

## 実機微調整中の文書更新

ユーザーがWinMUGEN実機を見ながら位置、倍率、速度、時間、色、透過、描画優先度などを微調整している間も、CNS、CMDまたはAIRの現行試験値を設計文書とステート文書へ同期し、試験中と注記する。実装と文書に差異がある場合はCNS、CMDまたはAIRを正本とし、実装値を変更せず文書を更新する。

ユーザーが検収結果を採用または確定した後は、値を維持したまま試験中の注記を外し、実装と文書の差異が残っていないことを確認する。

構文検査を越えるゲーム挙動テストを追加しない。`AGENTS.md`または`docs/DESIGN.md`を変更する場合は、事前にユーザーの承認を得る。
