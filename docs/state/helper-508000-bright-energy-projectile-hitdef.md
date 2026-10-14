# 明光弾攻撃判定Helper責務

## 攻撃判定

### StateDef 508900: 完成位置でのHitDef

各明光弾の生成から12tick後、寿命末尾20tickの縮小開始前までHitDefを設定する。相手が明光弾の左右どちらにいるかに応じてHelperの向きを合わせ、命中速度が相手を光弾から外側へ押す向きになるようにする。

一個当たりのDamageは`20,3`、Priorityは`3,hit`、PauseTimeは`4,4`である。地上・空中でガード可能とし、HitFlagは`MAF`、GuardFlagは`MA`、属性は`A,SP`とする。地上命中はSlideTime `8`、HitTime `10`、X速度`-4`、空中命中はHitTime `10`、速度`-3,-2.5`で、ダウンさせない。

命中またはガードを検出すると終了要求bitを設定する。処理後は両手光弾発出管理ルーターStateDef `599100`へ進む。

## 命中時終了

### StateDef 508910: HitDefによる終了要求

HitDefの`p1stateno`から進入し、終了要求bitを設定して共通寿命判定StateDef `599900`へ接続する。通常命中時に同じ光弾を再命中させないための即時終了経路である。

変数割当は[明光弾攻撃判定Helper変数](var-list-helper-508000.md)を参照する。
