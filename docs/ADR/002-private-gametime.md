# ADR 002: private-gametimeの導入

## 状態

採用

## 背景

`gametime` はゲーム全体の経過tickを返す。一方、TENKIKAIの周期運動や演出の時刻は、キャラクター固有の時間として管理できる必要がある。

## 決定

通常変数 `var(0)` を `private-gametime` として使用する。

StateDef `-2` で本体のゲーム開始直後に `0` へ初期化し、その後は毎tick `1` 加算する。これにより、ゲーム全体の `gametime` と同期して進むキャラクター固有の時間を提供する。

既存の `gametime` を参照していた処理は、`private-gametime` を参照する。

通常変数 `var(1)` を `private-time` として使用する。StateDef `-2` で本体の `time=0` を検知した直後に `0` へ初期化し、その後は毎tick `1` 加算する。StateDef内の `time` の代用品として使用する。

## 結果

TENKIKAIの周期運動と定期演出は、ゲーム全体の時刻ではなく `private-gametime` に基づいて評価される。ヘルパーから参照する場合も、本体の `private-gametime` を使用する。

StateDefの経過時間は `private-time` で参照でき、StateDefが変わるたびに初期化される。
