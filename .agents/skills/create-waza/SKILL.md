---
name: create-waza
description: TENKIKAIの技、攻撃、特殊移動、技に伴う演出を新規作成または変更する。WinMUGENのCNS、CMD、AIR、Helper、Explod、Projectile、入力、オートメーション、the_controller連携を扱う技作業で使用する。
---

# Create Waza

TENKIKAI固有の設計とWinMUGENの実行順を維持する。関連文書は必要なものだけを読む。

## 調査範囲を決める

1. ルートの`AGENTS.md`へ従う。
2. 入力、移動、攻撃判定、アニメーション、Helper、全体演出のうち対象要素を特定し、`rg`で関連するStateDef、Action、変数、文書を探す。
3. `docs/DESIGN.md`、`docs/design/`、後述の条件別文書から該当箇所だけを読む。
4. 対象コードと`docs/state/`を照合する。差異は自動解消せず、具体的にユーザーへ提示する。

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
| AngleDrawの解除・共有 | [ADR 010](../../../docs/ADR/010-angledraw-reset.md)、[ADR 020](../../../docs/ADR/020-controller-angledraw-sharing.md) |
| HeadとHead Auraの位置、変換、表示、残像 | [ADR 023](../../../docs/ADR/023-head-head-aura-transform-synchronization.md)、[ADR 024](../../../docs/ADR/024-head-head-aura-controller-managed-position-and-visibility.md) |
| Aura Bound | [Aura Bound設計](../../../docs/design/003-aura-bound.md) |
| エフェクトの追加・変更 | [エフェクト作業規則](../../../docs/AGENTS.effect.md)、[エフェクト設計一覧](../../../docs/design/008-effects.md)、対象個別文書。AllPalFXは[ADR 021](../../../docs/ADR/021-controller-allpalfx-routing.md)も読む |

## 技を設計する

実装前に次を確定する。既存の確定事項から求められない項目だけをユーザーへ確認する。

- StateDef、遷移元・遷移先、終了・中断時の復帰先
- 入力ビット、オートメーション判断、Action、素材、表示要素
- StateType、MoveType、Physics、Ctrl、座標、速度、時間、移動式
- HitDef、Helper、Explod、Projectile、ダメージ、Power、無敵、PlayerPush
- `the_controller`へ渡す演出要求と発動時刻

新しいエフェクト種別または表現パターンは、CNS実装前に一覧へ登録し、個別設計文書を作成または更新する。

Commandを直接参照できるのはStateDef `-1`の入力ビット変換だけとする。技遷移と技中処理は入力ビットまたは状態情報を使用する。入力を追加する場合だけ`docs/AGENTS.input-map.md`、`docs/AGENTS.command.md`、`docs/AGENTS.automation.md`を読む。

## 実装と確認

1. ユーザーの未コミット変更を保持する。
2. CNS、CMD、AIRと必要な流動文書を同時に更新する。
3. 変数、StateDef、Action、Helper IDの衝突と、遷移・座標・速度・時間・ダメージを検証する。
4. `make check`を実行する。
5. WinMUGEN実機で確認すべき操作、表示、当たり判定をユーザーへ渡す。

構文検査を越えるゲーム挙動テストを追加しない。`AGENTS.md`または`docs/DESIGN.md`を変更する場合は、事前にユーザーの承認を得る。
