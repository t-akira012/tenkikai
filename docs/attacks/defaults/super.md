# super-v1

## 根拠

KFM StateDef `3000`のTriple Kung Fu Palmを多段型、StateDef `3050`のSmash Kung Fu Upperを単発型の基準とする。

## 共通試験候補

- State属性：`S, HA`
- SuperPause：使用する
- ガード可能
- 防御突破、アーマー、ReversalDef：なし
- 発動時無敵：KFM値を候補とするが、TENKIKAIでの対象属性と期間は個別承認する。

## 多段型

- Damage：中間打撃`72, 4`、最終打撃`75, 4`
- Priority：中間`6`、最終`5`
- PauseTime：`15, 15`
- Ground HitTime：`30`
- 最終打撃でFallを有効化する。
- Fall Recover：無効

## 単発型

- Damage：`155, 12`
- Priority：`5`
- PauseTime：`30, 30`
- Ground HitTime：`26`
- Ground/Air Velocity：`-1.3, -25`
- Fall：有効
- Fall Recover：無効
- Fall Damage：`70`

多段型と単発型の指定がない場合は、技の自然言語から確定する。判断できない場合はユーザーへ確認する。
