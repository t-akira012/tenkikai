# Trigger記述規則

## `command` 規則

### `command`はStateDef `-1`のビット変換処理に限り利用すること

WinMUGENでは、キャラクターはオートメーションで操作されるモードがある。

オートメーション中には`command`は入力されない。`command`を利用できるのは、StateDef `-1`でプレイヤー入力を通常変数のビットフラグへ変換する処理だけとする。技遷移、移動、速度増減などの処理は、StateDef `-1`を含め、`command`ではなく変換後のビットフラグをTriggerに使用する。詳細は[オートメーション規約](AGENTS.automation.md)を参照する。

### 入力非依存処理での `command` 禁止

`command`は、StateDef `-1`でプレイヤー入力をビットフラグへ変換する条件にのみ使用する。StateDef `-2`、StateDef `-3`、通常StateDef、Helper用StateDefでは、`command`をTriggerへ一切記述してはならない。

入力非依存処理には、`-2/-3`だけでなく、通常ステート内の重力・接地・状態同期・自動復帰・被弾処理なども含む。これらはオートメーション、入力を伴わないState遷移、被弾、State奪取からの復帰、ラウンド開始などでも成立しなければならない。入力情報である`command`に依存すると、条件が成立せず処理が停止する。

入力非依存処理の判定には、StateNo、StateType、位置、速度、時間、専用変数など、入力に依存しない状態情報を使用する。

### `triggerall` と `command`

`triggerall` に `command` トリガーを記述してはならない。

オートメーション中には`command`が入力されないため、`triggerall=command=...`を前提にした条件は成立しない。`command`を使用する場合は、StateDef `-1`のビット変換処理にある個別の`trigger1`、`trigger2`などへ記述する。

オートメーションにも対応させる処理では、変換後の入力・技フラグを使用する。入力非依存処理では、StateNo、StateType、位置、速度、時間、専用変数など、入力に依存しない状態情報を使用する。

## 時間トリガー

キャラクター固有の時間管理には通常の `gametime` を使用せず、`private-gametime`（[ADR 002](ADR/002-private-gametime.md)）を使用する。
