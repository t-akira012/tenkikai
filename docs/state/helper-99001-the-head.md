# the_head Helper

## StateDef 99001: 頭部追従

### 画面外移動許可

常駐Helperの`helpertype=player`を維持したまま、`ScreenBound value=0`で画面外への移動を許可する。カメラは追従させない。

### Root位置追従

Rootの位置へ毎フレーム追従する。

### Root向き同期

Rootの向きと`facing`を一致させるため、Rootに合わせて`Turn`する。

### Rootアニメーション同期

Rootのアニメーションを枚数と要素位置を含めて同期する。

### ダッシュ時の頭部位置移動

前後ダッシュに合わせて、頭部をダッシュ方向へ位置移動させる。Rootの向きと別の方向計算や符号補正は行わない。
