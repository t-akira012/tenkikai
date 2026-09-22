# the_head_aura Helper

## StateDef 99003000: 頭部Aura追従

### 画面外移動許可

常駐Helperの`helpertype=player`を維持したまま、`ScreenBound value=0`で画面外への移動を許可する。カメラは追従させない。

### 頭部位置追従

頭部Helperの完成位置を毎フレーム参照し、すべての状態で同じ位置へ追従する。位置計算を複製せず、Root基準の代替位置やStateDef固有の位置経路を持たない。

### Head Aura完成Offset

`the_controller`が保持するHead Aura完成OffsetのX値とY値を、一つの`Offset`で毎tick適用する。同期時はHead完成Offsetと同じ値を使用し、明示的なOffset非同期フラグが有効な場合だけHead Aura用の別の完成値を使用する。Head Aura自身はOffset式やRootのStateDefによる同期分岐を持たない。

### Root向き同期

Rootの向きと`facing`を一致させるため、Rootに合わせて`Turn`する。

### 頭部アニメーション同期

頭部Helperのアニメーションを枚数と要素位置を含めて同期する。

### 表示と残像

`the_controller`のHead Aura非表示ビットが有効な場合は頭部Auraを非表示にする。Head Aura残像非表示ビットが有効な場合は`AfterImageTime time=0`で残像を非表示にし、内部の残像生成済みフラグを`0`へ戻す。残像非表示ビットが無効な場合は通常のAfterImage表示を行う。Head Aura自身はRootのStateNoを判定しない。

頭部Aura自身はAngleDraw値を計算せず、`the_controller`が保持するHead Aura完成角度、X倍率、Y倍率を一つの`AngleDraw`で毎tick使用する。同期時はHead完成AngleDrawと同じ値を使用し、通常のAura倍率またはAura BoundによるAngleDraw非同期フラグが有効な場合だけHead Aura用の別の完成値を使用する。

## StateDef 99003999: 最終処理

頭部Aura追従の完了後に`SelfState value=5150`を実行する。
