# 技仕様とState Controllerの対応

この文書は実装手段の候補を示す。仕様項目からControllerを機械的に一対一変換する規則ではない。

| スキーマ | 主な実装候補 | 確認事項 |
| --- | --- | --- |
| 1-1 本体の動作 | `ChangeState`、`ChangeAnim`、`VelSet`、`VelAdd`、`VelMul`、`PosSet`、`PosAdd`、`Turn`、`CtrlSet` | 移動規約、浮遊、復帰・中断経路 |
| 1-2 主表現 | `Helper`、`Projectile`、`Explod`、`AngleDraw`、`BindToRoot`、`BindToParent` | 責務、ID、座標系、寿命、親消失後の挙動 |
| 1-3 付随エフェクト | `Explod`、`AfterImage`、`PalFX`、`AllPalFX`、`BgPalFX`、`EnvShake`、`PlaySnd` | 共通エフェクト再利用、優先度、有限寿命 |
| 2-1-1 判定 | `HitDef`、`Projectile`、非表示Projectile | Clsn、対象、発生・持続 |
| 2-1-2 威力・リソース | `damage`、`poweradd`、`getpower`、`givepower`、`juggle` | 本体と攻撃主体のどちらが所有するか |
| 2-1-3 攻撃属性 | `attr`、`guardflag`、`hitflag`、`priority` | 立ち・屈み・空中、通常・必殺・超必殺 |
| 2-1-4 防御突破特性 | 専用Helper、Projectile、Var/FVar、相手状態の観測 | WinMUGEN標準だけで表現可能か、外部互換性 |
| 2-1-5 持続・再命中・相殺 | `hitonce`、`miss.time`、Projectile設定、Helper寿命 | 多段化、再命中間隔、相殺後の消滅 |
| 2-2-1 無敵 | `the_controller`への要求、`NotHitBy`、`HitBy` | 既存の無敵管理責務を複製しない |
| 2-2-2 アーマー | Helper Armor、`HitOverride`、Var/FVar | 仮想ライフ、受付間隔、解除条件 |
| 2-2-3 ReversalDef | `ReversalDef`、成功監視、`ChangeState` | 受付属性、成功時の対象、State奪取 |
| 2-2-4 移動・位置制御 | 速度Controller、`PosSet`、`TargetBind`、`BindToRoot` | 慣性、座標系、拘束解除 |
| 2-2-5 その他 | `PlayerPush`、`PowerAdd`、`PowerSet`、`CtrlSet`、入力ビット | 発動条件、消費時刻、キャンセル可否 |
| 2-3-1 通常命中時作用 | HitDef/Projectileの速度・硬直・`fall`、`TargetState` | 地上・空中差、追撃可否 |
| 2-3-2 ガード時作用 | `guard.velocity`、`guard.hittime`、削り値 | ガード方向、押し戻し、削り |
| 2-3-3 特殊命中時作用 | `TargetState`、`TargetBind`、`TargetLifeAdd`、専用StateDef | 相手を戻す経路、中断時の安全性 |

## 特殊実装の記録

標準Controllerだけで仕様を表現できない場合は、個別技文書の「実装対応」に次を記録する。

- 標準Controllerだけでは成立しない理由
- 使用するRoot、Helper、Projectileの責務
- Var/FVarの所有者、番号、寿命、初期化
- `the_controller`との要求・完成値の受け渡し
- 外部キャラクターに依存する場合の互換性範囲
