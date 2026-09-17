# ADR 002: private-gametimeの導入

## 状態

採用

## 背景

`gametime` はゲーム全体の経過tickを返す。一方、TENKIKAIの周期運動や演出の時刻は、キャラクター固有の時間として管理できる必要がある。

## 決定

### private-gametime

通常変数 `var(0)` を `private-gametime` として使用する。

StateDef `-2` で本体のゲーム開始直後に `0` へ初期化し、その後は毎tick `1` 加算する。これにより、ゲーム全体の `gametime` と同期して進むキャラクター固有の時間を提供する。

既存の `gametime` を参照していた処理は、`private-gametime` を参照する。

### private-time

通常変数 `var(1)` を `private-time` として使用する。`private-time` の管理をRootの`-2/-3`から外し、`the_controller` が親Rootを監視して更新する。

- `the_controller` が `root,time=0` を検知する
- `ParentVarSet` で親の `var(1)` を0へ初期化する
- 次tick以降は `ParentVarAdd` で親の `var(1)` を1ずつ加算する
- `-2/-3` には`private-time`の初期化・加算処理を置かない
- 同じControllerがRootのStateDef監視と`private-time`管理を担う

これにより、StateDef遷移直後をController自身が直接検知でき、`-2`の処理順に依存しない。`private-time` はStateDef内の`time`の代用品として使用する。

`private-gametime`、`private-time`、およびAfterImage制御に使用する `var(10)` はラウンド間で持ち越さない。`cns/constants.cns` の `IntPersistIndex=50` により、これらを含む変数スロット `var(0)`～`var(49)` はラウンド開始時に0へリセットされる。別の試合へも持ち越さない。

## 結果

### private-gametime

TENKIKAIの周期運動と定期演出は、ゲーム全体の時刻ではなく `private-gametime` に基づいて評価される。ヘルパーから参照する場合も、本体の `private-gametime` を使用する。

### private-time

StateDefの経過時間は `private-time` で参照でき、StateDefが変わるたびに初期化される。

ラウンド開始時には `private-gametime` と `private-time` が初期状態から再開し、AfterImageの初回生成制御も `var(10)` のリセットによって再実行可能になる。
