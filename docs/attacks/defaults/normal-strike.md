# normal-strike-v1

## 根拠

KFM StateDef `200`の立ち弱パンチを軽攻撃、StateDef `210`の立ち強パンチを強攻撃の基準とする。

## 軽攻撃

- State属性：`S, NA`
- Damage：`23, 0`
- Power加算：`20`
- Juggle：`1`
- GuardFlag：`MA`
- HitFlag：`MAF`
- Priority：`3, Hit`
- PauseTime：`8, 8`
- Ground SlideTime：`5`
- Ground HitTime：`10`
- Ground Velocity：`-4, 0`
- Air Velocity：`-1.4, -3`
- Air HitTime：`12`
- 防御突破、無敵、アーマー、ReversalDef：なし

## 強攻撃

- State属性：`S, NA`
- Damage：`57, 0`
- Power加算：`65`
- Juggle：`4`
- GuardFlag：`MA`
- Priority：既定値
- PauseTime：`12, 12`
- Ground SlideTime：`12`
- Ground HitTime：`13`
- Ground Velocity：`-5.5, 0`
- Air Velocity：`-2.5, -4`
- 防御突破、無敵、アーマー、ReversalDef：なし

軽重の指定がない場合は、威力または動作の自然言語から確定する。判断できない場合はユーザーへ確認する。
