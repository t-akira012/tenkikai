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

`private-time`は廃止し、StateDef経過時間には`time`を使用する。

`private-gametime`およびAfterImage制御に使用する `var(10)` はラウンド間で持ち越さない。`cns/constants.cns` の `IntPersistIndex=50` により、これらを含む変数スロット `var(0)`～`var(49)` はラウンド開始時に0へリセットされる。別の試合へも持ち越さない。

## 結果

### private-gametime

TENKIKAIの周期運動と定期演出は、ゲーム全体の時刻ではなく `private-gametime` に基づいて評価される。ヘルパーから参照する場合も、本体の `private-gametime` を使用する。

ラウンド開始時には `private-gametime` が初期状態から再開し、AfterImageの初回生成制御も `var(10)` のリセットによって再実行可能になる。
