# the_head_aura Helper

## StateDef 99003000: 頭部Aura追従

### 画面外移動許可

常駐Helperの`helpertype=player`を維持したまま、`ScreenBound value=0`で画面外への移動を許可する。カメラは追従させない。

### 頭部位置追従

頭部Helperの位置へ毎フレーム追従する。

### Root向き同期

Rootの向きと`facing`を一致させるため、Rootに合わせて`Turn`する。

### 頭部アニメーション同期

頭部Helperのアニメーションを枚数と要素位置を含めて同期する。

### ダッシュ時の頭部位置移動

前後ダッシュに合わせて、頭部Auraを頭部と同じ方向へ位置移動させる。

## StateDef 99003999: 最終処理

頭部Aura追従の完了後に`SelfState value=5150`を実行する。
