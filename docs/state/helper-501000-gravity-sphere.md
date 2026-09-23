# 重力球Helper

## StateDef 501000: 汎用重力球

StateDef `1100`の`private-time=12`で、Root前方45px・上方50pxへHelper ID `501000`として生成する試験実装である。Helperは発生元から独立し、前方へ`3px/tick`で移動して自身の`time>=120`で消滅する。

球体はAction `18552`をX・Yともに`0.25`倍で表示する。Helper本体へ減算合成を適用し、時間120tick、最大12枚の減算AfterImageを重ねる。描画優先順位は`5`とする。

寿命中は2tickごとにExplod ID `501100`、Action `18553`の光を生成する。生成角度はHelper自身の`time`を基準に1tickあたり24度進み、球体を中心とするX半径28px・Y半径18pxの楕円上から発生する。光の速度は外向き`0.8px/tick`と接線方向`1.5px/tick`を合成し、生成後は球体へBindしない。

周回位置が球体の奥側にある場合は描画優先順位`4`、手前側にある場合は`6`とする。光は加算合成し、Action `18553`の終了時に消滅する。

HelperはPlayerPush、被弾、画面追従、影および`HitDef`を持たない。ラウンド終了時は寿命を待たずに消滅する。

## 予約範囲

- 重力球専用StateDef：`501000`〜`501999`
- 汎用重力球Helper ID・StateDef：`501000`
- 周回光Explod ID：`501100`
