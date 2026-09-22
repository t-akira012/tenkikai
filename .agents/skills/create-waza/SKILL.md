---
name: create-waza
description: TENKIKAIの技、攻撃、特殊移動、技に伴う演出を新規作成または変更する。WinMUGENのCNS、CMD、AIR、Helper、Explod、Projectile、入力、オートメーション、the_controller連携を扱う技作業で使用する。
---

# Create Waza

TENKIKAI固有の設計とWinMUGENの実行順を維持して技を作成する。必要な箇所だけを読み、関連しない文書を一括で読み込まない。

## 調査範囲を決める

1. ルートの`AGENTS.md`へ従う。
2. ユーザー要求から、入力、移動、攻撃判定、アニメーション、Helper、全体演出のうち必要な要素を特定する。
3. `rg`で関連するStateDef、Action、変数、既存文書を検索し、該当箇所だけを読む。
4. `docs/DESIGN.md`と`docs/design/`から、技に関係する確定済み方針だけを読む。
5. 対象のCNS・CMD・AIRと対応する`docs/state/`文書を照合する。差異がある場合は、どちらかへ自動的に合わせずユーザーへ提示する。

上位設計にない見た目、時間、速度、ダメージ、無敵、色、軌道を推測で確定しない。美的判断またはゲームバランスの判断が必要な場合は実装前に確認する。

## the_controllerの責務

`the_controller`は本リポジトリ固有の統合制御Helperである。技が次の処理を必要とする場合は、Rootの技StateDefへ処理を分散させず、既存の`the_controller`責務を使用する。

- Helper Armorによる攻撃受付と仮想ライフ処理
- PlayerPushの有効・無効
- 技中の無敵
- Rootアニメーション番号と開始時時間の共有
- Body、Head、Aura間のAngleDraw値と適用対象の共有
- Aura Bound
- AllPalFXによる全画面の暗転、発光、色変更
- Rootと複数Helperへまたがる技演出の監視と値共有

新しい技が既存責務に該当する場合は、新しい管理HelperやRoot側の重複処理を作らない。既存責務に該当しない全体制御を`the_controller`へ追加する場合は、責務の追加をユーザーへ提示する。

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
- 個別挙動が成立しない経路を次の挙動塊へ接続する。
- 個別挙動が成立する経路も、処理後に同じ次の挙動塊へ接続する。
- 挙動塊同士を排他的な分岐として扱わず、常に固定順で通過させる。
- 最後の挙動塊だけを終端へ接続する。
- 個別挙動から集約StateDefへ直接戻さない。
- 新しい挙動塊を追加する場合は、配置する順序を確定し、直前と直後の挙動塊へ両経路を接続する。

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
| AngleDrawの解除 | [ADR 010](../../../docs/ADR/010-angledraw-reset.md) |
| 複数表示要素のAngleDraw共有 | [ADR 020](../../../docs/ADR/020-controller-angledraw-sharing.md) |
| Aura Bound | [Aura Bound設計](../../../docs/design/003-aura-bound.md) |
| AllPalFX暗転 | [ADR 021](../../../docs/ADR/021-controller-allpalfx-routing.md) |

## 技を設計する

実装前に次を確定する。既存の確定事項から求められない項目だけをユーザーへ確認する。

- StateDef番号と遷移元・遷移先
- プレイヤー入力ビットとオートメーション判断
- Action番号、素材、表示要素
- StateType、MoveType、Physics、Ctrl
- 座標、速度、時間、移動式
- HitDef、Helper、Explod、Projectileの要否
- ダメージ、Power、無敵、PlayerPush
- `the_controller`へ渡す演出要求と発動時刻
- 技終了時と中断時の復帰先

Commandを直接参照できるのはStateDef `-1`の入力ビット変換だけとする。技遷移と技中処理は入力ビットまたは状態情報を使用する。入力を追加する場合だけ`docs/AGENTS.input-map.md`、`docs/AGENTS.command.md`、`docs/AGENTS.automation.md`を読む。

## 実装と確認

1. ユーザーの未コミット変更を保持する。
2. CNS、CMD、AIRと必要な流動文書を同時に更新する。
3. 変数、StateDef、Action、Helper IDの衝突を`rg`で確認する。
4. 遷移条件、座標、速度、時間、ダメージを数学的に検証する。
5. `make check`を実行する。
6. WinMUGEN実機で確認すべき操作、表示、当たり判定をユーザーへ渡す。

構文検査を越えるゲーム挙動テストを追加しない。`AGENTS.md`または`docs/DESIGN.md`を変更する場合は、事前にユーザーの承認を得る。
