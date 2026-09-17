# GetHitVar()

## ユーザー調査で確認された仕様

`GetHitVar(文字列)`は、直前に受けた攻撃の内部情報を参照する。値は攻撃を受けた後も内部に保持され、新しい攻撃または対応する処理によって更新・リセットされる。実際の状態処理はCommonステートで行われるものが多い。

### くらいモーション

- `AnimType`：攻撃のアニメーション属性。`0` light、`1` medium、`2` hard、`3` back、`4` up、`5` diag-up。
- `GroundType`：地上攻撃ののけぞり属性。`0` non、`1` high、`2` low、`3` trip。
- `AirType`：空中攻撃ののけぞり属性。`0` non、`1` high、`2` low。

### 威力・硬直

- `Damage`：ダメージを受ける1フレームだけ、今回のダメージ量を返す。
- `HitShakeTime`：ヒットポーズ中の残り時間。毎フレーム減算され、`0`になると`HitShakeOver`が成立する。
- `HitTime`：ヒットポーズ後の残り硬直時間。毎フレーム減算され、`-1`になると`HitOver`が成立する。
- `SlideTime`：地上ノックバック減速を開始する基準時間。Commonステートで使用される。
- `CtrlTime`：ガード中に`Ctrl=1`へ移行する基準時間。Commonステートで使用される。
- `RecoverTime`：倒れ待機時間。操作によって短縮され、1回の操作で残り時間に`3/4`を乗じる。

`HitShakeTime`と`HitTime`の合計から、ヒット時の残り硬直を確認できる。`MoveType`がくらい状態から変化した場合、これらの時間が短期間で`0`になることがある。

### 回数

- `HitCount`：連続してヒットした回数。ガードでは加算されない。
- `FallCount`：バウンドした回数。Trip属性では着地前に1加算される。

`HitCount`は、くらい状態以外から新たにヒットした場合にリセットされる。ガードではリセットされないため、ガード硬直から続けて攻撃を受けると、直前のコンボ分を含んだ値になる。

### 速度

- `XVel`：ノックバックX速度。絶対座標方向の値であり、実際の移動方向は`Facing`との積で決まる。
- `YVel`：吹っ飛びY速度。`HitVelSet`で使用される。
- `YAccel`：攻撃から渡された落下加速度。Commonステートの重力処理で使用される。

### Fall情報

- `Fall`：倒れ判定。`0`になると自動受身着地の処理対象になる。
- `Fall.Damage`：`HitFallDamage`で減少させる値。`HitFallDamage`実行時にリセットされる。
- `Fall.XVel`、`Fall.YVel`：落下バウンド時の速度。`HitFallVel`で使用される。
- `Fall.Recover`：受身可能かどうか。
- `Fall.RecoverTime`：受身可能になるまでの内部時間。`CanRecover`の判定に使用される。
- `Fall.Kill`：`Fall.Kill`の設定値を返すが、実際の処理上は意味を持たない。
- `Fall.EnvShake.Time`、`Fall.EnvShake.Freq`、`Fall.EnvShake.Ampl`、`Fall.EnvShake.Phase`：攻撃から渡された落下時画面揺れの設定値。

### その他

- `ChainID`：攻撃のChainID。
- `Guarded`：今回の攻撃をガードしたかどうか。
- `IsBound`：`TargetBind`の影響を受けている間に成立する情報。通常のTrigger索引にはないが、参照できる。

`XVelAdd`、`YVelAdd`、`Type`、`XOff`、`YOff`は、通常の状態制御では使用されないか、仕様が確認されていない。

## 原典

[GetHitVar - MUGEN CNS WIKI CHAOS@予定](https://w.atwiki.jp/mugencns/pages/126.html)
