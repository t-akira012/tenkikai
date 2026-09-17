# HitOverride

## ユーザー調査で確認された仕様

`HitOverride`が発動すると、対象属性の攻撃から抜け、相手の攻撃自体はヒット扱いになる。発動したキャラクターは相手側から`Target`を取得されない。

`HitOverride`の対象となる攻撃は、`HitDef`、`Projectile`、`ReversalDef`による攻撃である。発動条件は、攻撃側の攻撃属性と受け側の`HitOverride`に指定した属性が一致することである。攻撃属性はStateType属性と攻撃属性の双方で判定される。

## P1StateNo・P2GetP1Stateとの関係

対象属性の攻撃にP1StateNo指定、または`P2GetP1State=1`指定がある場合、`HitOverride`の対象にはならず攻撃も当たらない。

攻撃にP2StateNoが記述されていても、`P2GetP1State=0`であれば通常どおり攻撃が当たり、`HitOverride`が発動する。

## StateNo指定と処理時点

`StateNo`を指定した場合、攻撃命中による通常のくらいステートへの移動後、その指定ステートへの移動で上書きされる。移動後の`PrevStateNo`には、上書き前の通常くらいステート番号が記録される。

`StateNo=-1`では通常のくらいステートに留まるが、`Target`は取得されない。移動後も`MoveType=H`である間はダメージを受ける。`MoveType`をくらい状態以外へ変更した場合は、攻撃によるダメージを無効化できる。

`HitOverride`はガード可能な状態でも、指定属性との一致条件が成立すれば発動する。この場合も相手の攻撃はヒット扱いになる。

## 原典

[HitOverride - MUGEN CNS WIKI CHAOS@予定](https://w.atwiki.jp/mugencns/pages/239.html)
