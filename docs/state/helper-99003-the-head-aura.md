# the_head_aura Helper

## StateDef 99003000: 頭部Aura追従

### 画面外移動許可

常駐Helperの`helpertype=player`を維持したまま、`ScreenBound value=0`で画面外への移動を許可する。カメラは追従させない。

### 頭部位置追従

通常時は頭部Helperの位置へ毎フレーム追従する。RootがStateDef `300`の場合はHelper間の処理順による1 tickの位置遅延を避けるため、Root位置を基準に頭部と同じ位置補正を同一tickで適用する。通常の浮遊Offsetは適用せず、アニメーション中心へ移動する頭部と表示位置を揃える。

### Root向き同期

Rootの向きと`facing`を一致させるため、Rootに合わせて`Turn`する。

### 頭部アニメーション同期

頭部Helperのアニメーションを枚数と要素位置を含めて同期する。

### ダッシュ時の頭部位置移動

前後ダッシュに合わせて、頭部Auraを頭部と同じ方向へ位置移動させる。

### 異形回避中の表示

RootがStateDef `300`の場合は頭部Auraを表示したまま残像を消去する。StateDef `301`では頭部Auraを非表示にする。StateDef `302`で残像の初回生成フラグを解除し、再出現後の残像を再開する。

頭部Aura自身は共有AngleDraw値を計算しない。`the_controller`のHead Aura適用フラグが有効で、Aura Boundフラグが無効な場合だけ、Controllerが保持する角度、X倍率、Y倍率の完成値を使用する。Aura Bound中は既存のAura倍率を優先する。

## StateDef 99003999: 最終処理

頭部Aura追従の完了後に`SelfState value=5150`を実行する。
